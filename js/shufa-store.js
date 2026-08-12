// 临池录共享存储层：练习记录 + 库存 的读写/草稿/同步（供各页面复用）
(function () {
  const REPO = 'Charlottttttttttttte/personal-site';
  const FILES = {
    records: { path: 'data/shufa-records.json', lsKey: 'shufa_records_local' },
    inventory: { path: 'data/shufa-inventory.json', lsKey: 'shufa_inv_local' }
  };
  const LS_TOKEN = 'shufa_gh_token';

  async function fetchWithTimeout(url, ms) {
    const ctrl = new AbortController();
    const t = setTimeout(() => ctrl.abort(), ms);
    try { return await fetch(url, { signal: ctrl.signal }); }
    finally { clearTimeout(t); }
  }

  // 从网站/API 加载某个数据文件（无草稿时）
  async function loadFromGitHub(kind) {
    const f = FILES[kind];
    // 通道1: 同站
    try {
      const r = await fetchWithTimeout(f.path, 8000);
      if (!r.ok) throw new Error('HTTP ' + r.status);
      return await r.json();
    } catch (e1) {
      // 通道2: API
      try {
        const r = await fetchWithTimeout(`https://api.github.com/repos/${REPO}/contents/${f.path}`, 10000);
        if (!r.ok) throw new Error('HTTP ' + r.status);
        const meta = await r.json();
        const bin = atob(meta.content);
        const bytes = new Uint8Array(bin.length);
        for (let i = 0; i < bin.length; i++) bytes[i] = bin.charCodeAt(i);
        return JSON.parse(new TextDecoder().decode(bytes));
      } catch (e2) {
        throw new Error(e1.message + ' / ' + e2.message);
      }
    }
  }

  // 读取（草稿优先）
  async function load(kind) {
    const f = FILES[kind];
    const draft = localStorage.getItem(f.lsKey);
    if (draft) {
      try { return { data: JSON.parse(draft), fromDraft: true }; }
      catch (e) { /* 草稿损坏则忽略 */ }
    }
    const data = await loadFromGitHub(kind);
    return { data, fromDraft: false };
  }

  function saveDraft(kind, data) {
    localStorage.setItem(FILES[kind].lsKey, JSON.stringify(data));
  }

  function clearDraft(kind) {
    localStorage.removeItem(FILES[kind].lsKey);
  }

  function getToken() { return localStorage.getItem(LS_TOKEN) || ''; }
  function setToken(t) { localStorage.setItem(LS_TOKEN, t); }

  function utf8ToBase64(str) {
    const bytes = new TextEncoder().encode(str);
    let bin = '';
    bytes.forEach(b => bin += String.fromCharCode(b));
    return btoa(bin);
  }

  // 一键同步单个数据文件到 GitHub
  async function syncToGitHub(kind, data, message) {
    const token = getToken();
    if (!token) throw new Error('未设置令牌，请先点 🔑 设置');
    const f = FILES[kind];
    const api = `https://api.github.com/repos/${REPO}/contents/${f.path}`;
    const headers = { 'Authorization': 'Bearer ' + token, 'Accept': 'application/vnd.github+json' };
    let sha = null;
    try {
      const g = await fetchWithTimeout(api, 10000);
      if (g.ok) sha = (await g.json()).sha;
      else if (g.status !== 404) throw new Error('读取失败 HTTP ' + g.status);
    } catch (e) { throw new Error('读取失败：' + e.message); }

    const content = utf8ToBase64(JSON.stringify(data, null, 2));
    const body = { message: message || ('同步 ' + new Date().toISOString().slice(0, 10)), content };
    if (sha) body.sha = sha;

    const p = await fetchWithTimeout(api, 15000).catch(e => { throw new Error('网络错误：' + e.message); });
    const resp = await fetch(api, {
      method: 'PUT',
      headers: { ...headers, 'Content-Type': 'application/json' },
      body: JSON.stringify(body)
    });
    if (!resp.ok) {
      const err = await resp.json().catch(() => ({}));
      throw new Error('写入失败 HTTP ' + resp.status + (err.message ? '：' + err.message : ''));
    }
    clearDraft(kind);
    return true;
  }

  window.SHUFA_STORE = {
    REPO, FILES, load, saveDraft, clearDraft, getToken, setToken, syncToGitHub
  };
})();
