// 临池录共享存储层：练习记录 + 库存 + 自定义字帖 的读写/草稿/同步（供各页面复用）
(function () {
  const REPO = 'Charlottttttttttttte/personal-site';
  const FILES = {
    records: { path: 'data/shufa-records.json', lsKey: 'shufa_records_local' },
    inventory: { path: 'data/shufa-inventory.json', lsKey: 'shufa_inv_local' },
    customCopybooks: { path: 'data/shufa-custom-copybooks.json', lsKey: 'shufa_custom_copybooks' }
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

  // ---------- 自定义字帖（本机持久化 + GitHub 同步） ----------
  const LS_CUSTOM_COPYBOOKS = FILES.customCopybooks.lsKey;

  function getCustomCopybooks() {
    try {
      const list = JSON.parse(localStorage.getItem(LS_CUSTOM_COPYBOOKS));
      return Array.isArray(list) ? list : [];
    } catch (e) { return []; }
  }

  // 按名称去重；fontId/fontName 可空（未选字体时）
  function addCustomCopybook(name, fontId, fontName) {
    const trimmed = String(name || '').trim();
    if (!trimmed) return null;
    const list = getCustomCopybooks();
    const existing = list.find(b => b.copybookName === trimmed);
    if (existing) {
      if (fontId && !existing.fontId) { existing.fontId = fontId; existing.fontName = fontName; }
      localStorage.setItem(LS_CUSTOM_COPYBOOKS, JSON.stringify(list));
      return existing;
    }
    const entry = {
      copybookId: 'custom:' + trimmed,
      copybookName: trimmed,
      fontId: fontId || '',
      fontName: fontName || '',
      authorId: 'custom',
      authorName: '自定义'
    };
    list.push(entry);
    localStorage.setItem(LS_CUSTOM_COPYBOOKS, JSON.stringify(list));
    return entry;
  }

  // 合并两份字帖列表（本机优先），按名称去重并规范化 id
  function mergeCustomLists(local, remote) {
    const merged = [];
    const seen = new Set();
    for (const list of [local, remote]) {
      for (const b of list) {
        if (!b || !b.copybookName || seen.has(b.copybookName)) continue;
        seen.add(b.copybookName);
        merged.push({ ...b, copybookId: 'custom:' + b.copybookName });
      }
    }
    return merged;
  }

  // 同步自定义字帖：拉取线上 → 与本机合并去重 → 写回本机 + GitHub
  // 双向合并，多设备各加各的互不覆盖
  async function syncCustomCopybooks() {
    let remote = [];
    try {
      const r = await loadFromGitHub('customCopybooks');
      if (r && Array.isArray(r.items)) remote = r.items;
    } catch (e) {
      // 线上文件不存在（404）视为空；其它拉取失败不覆盖线上，直接中断
      if (!String(e.message).includes('404')) throw e;
    }
    const merged = mergeCustomLists(getCustomCopybooks(), remote);
    localStorage.setItem(LS_CUSTOM_COPYBOOKS, JSON.stringify(merged));
    await syncToGitHub('customCopybooks',
      { updatedAt: new Date().toISOString().slice(0, 10), items: merged },
      '字帖同步 ' + new Date().toISOString().slice(0, 10),
      true /* 本机为配置存储，不清草稿 */);
    return merged;
  }

  // 仅拉取线上字帖合并到本机（静默，供记录页启动时调用；失败忽略）
  async function pullCustomCopybooks() {
    let remote = [];
    try {
      const r = await loadFromGitHub('customCopybooks');
      if (r && Array.isArray(r.items)) remote = r.items;
    } catch (e) { return; }
    if (!remote.length) return;
    const merged = mergeCustomLists(getCustomCopybooks(), remote);
    localStorage.setItem(LS_CUSTOM_COPYBOOKS, JSON.stringify(merged));
    return merged;
  }

  function getToken() { return localStorage.getItem(LS_TOKEN) || ''; }
  function setToken(t) { localStorage.setItem(LS_TOKEN, t); }

  function utf8ToBase64(str) {
    const bytes = new TextEncoder().encode(str);
    let bin = '';
    bytes.forEach(b => bin += String.fromCharCode(b));
    return btoa(bin);
  }

  // 一键同步单个数据文件到 GitHub；keepDraft=true 时不清理本地（用于自定义字帖等"配置型"数据）
  async function syncToGitHub(kind, data, message, keepDraft) {
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
    if (!keepDraft) clearDraft(kind);
    return true;
  }

  // 按 id 合并两份列表：本机优先，线上补充（防多设备互覆盖、补全线上新增）
  function mergeById(localItems, remoteItems) {
    const merged = [];
    const seen = new Set();
    for (const list of [localItems, remoteItems]) {
      for (const it of list) {
        if (!it || !it.id || seen.has(it.id)) continue;
        seen.add(it.id);
        merged.push(it);
      }
    }
    return merged;
  }

  // 合并同步单个数据文件：拉线上 → 按 id 合并 → 上传 → 写回本机草稿
  // 本机草稿保留：页面始终显示本机最新数据，不依赖线上部署延迟
  async function mergeSync(kind, local, message) {
    let remote = null;
    try {
      const r = await loadFromGitHub(kind);
      remote = r;
    } catch (e) {
      if (!String(e.message).includes('404')) throw e;
    }
    const listKey = kind === 'records' ? 'records' : 'items';
    const merged = {
      updatedAt: new Date().toISOString().slice(0, 10),
      [listKey]: mergeById(local[listKey] || [], (remote && remote[listKey]) || [])
    };
    await syncToGitHub(kind, merged, message, true /* 保留本机草稿 */);
    localStorage.setItem(FILES[kind].lsKey, JSON.stringify(merged));
    return merged;
  }

  // 一键同步全部数据（记录 + 库存 + 自定义字帖）。dataProvider: { records: data, inventory: data|null }
  // 未提供的数据文件会读本机草稿；无草稿则跳过（不空写覆盖线上）；自定义字帖总是双向合并同步
  async function syncAll(dataProvider) {
    const token = getToken();
    if (!token) throw new Error('未设置令牌，请先点 🔑 设置');
    const dateStr = new Date().toISOString().slice(0, 10);
    const results = [];

    // 1) 记录
    let recData = null;
    if (dataProvider && dataProvider.records) {
      recData = dataProvider.records;
    } else {
      const d = localStorage.getItem(FILES.records.lsKey);
      if (d) recData = JSON.parse(d);
    }
    if (recData) {
      await mergeSync('records', recData, '记录同步 ' + dateStr);
      results.push('记录');
    }

    // 2) 库存
    let invData = null;
    if (dataProvider && dataProvider.inventory) {
      invData = dataProvider.inventory;
    } else {
      const d = localStorage.getItem(FILES.inventory.lsKey);
      if (d) invData = JSON.parse(d);
    }
    if (invData) {
      await mergeSync('inventory', invData, '库存同步 ' + dateStr);
      results.push('库存');
    }

    // 3) 自定义字帖：总是合并同步（多设备双向，新增/拉取互不覆盖）
    try {
      await syncCustomCopybooks();
      results.push('字帖');
    } catch (e) {
      throw new Error('字帖同步失败：' + e.message);
    }

    if (!results.length) {
      // 没有草稿：拉取线上再写回（确保 updatedAt 刷新），或提示无改动
      return { synced: [], note: '无本地改动' };
    }
    return { synced: results };
  }

  window.SHUFA_STORE = {
    REPO, FILES, load, saveDraft, clearDraft, getToken, setToken, syncToGitHub, syncAll,
    getCustomCopybooks, addCustomCopybook, syncCustomCopybooks, pullCustomCopybooks
  };
})();
