// 临池录自然语言解析器（移植自小程序 utils/parser.js，依赖 window.SHUFA_DATA）
(function () {
  const D = window.SHUFA_DATA;
  if (!D) { console.error('shufa-data.js 未加载'); return; }
  const PAPER_KEYWORDS = D.PAPER_KEYWORDS;
  const FONT_KEYWORDS = D.FONT_KEYWORDS;
  const COPYBOOK_LIST = D.COPYBOOK_LIST;
  const PAPER_TYPES = D.PAPER_TYPES;

  // ==================== 中文数字转换 ====================
  const CN_NUM_MAP = {
    '一': 1, '二': 2, '两': 2, '三': 3, '四': 4, '五': 5,
    '六': 6, '七': 7, '八': 8, '九': 9, '十': 10,
    '百': 100, '千': 1000
  };

  function chineseToNumber(str) {
    if (!str) return 0;
    str = str.trim();
    if (/^\d+$/.test(str)) return parseInt(str, 10);
    let result = 0;
    let temp = 0;
    for (let i = 0; i < str.length; i++) {
      const ch = str[i];
      const val = CN_NUM_MAP[ch];
      if (val === undefined) continue;
      if (val >= 10) {
        if (temp === 0) temp = 1;
        result += temp * val;
        temp = 0;
      } else {
        temp = temp * 10 + val;
      }
    }
    return result + temp;
  }

  // ==================== 模糊匹配（Levenshtein 距离）====================
  function levenshtein(a, b) {
    const matrix = [];
    for (let i = 0; i <= b.length; i++) matrix[i] = [i];
    for (let j = 0; j <= a.length; j++) matrix[0][j] = j;
    for (let i = 1; i <= b.length; i++) {
      for (let j = 1; j <= a.length; j++) {
        if (b.charAt(i - 1) === a.charAt(j - 1)) {
          matrix[i][j] = matrix[i - 1][j - 1];
        } else {
          matrix[i][j] = Math.min(
            matrix[i - 1][j - 1] + 1,
            matrix[i][j - 1] + 1,
            matrix[i - 1][j] + 1
          );
        }
      }
    }
    return matrix[b.length][a.length];
  }

  function fuzzyMatchScore(text, target) {
    text = text.toLowerCase();
    target = target.toLowerCase();
    if (text.includes(target)) return 1.0;
    if (target.includes(text)) return 0.9;
    const dist = levenshtein(text, target);
    const maxLen = Math.max(text.length, target.length);
    if (maxLen === 0) return 1.0;
    const similarity = 1 - dist / maxLen;
    return similarity > 0.5 ? similarity : 0;
  }

  // ==================== 解析器核心 ====================
  const parser = {
    extractPaper(text) {
      if (!text) return null;
      for (const item of PAPER_KEYWORDS) {
        for (const kw of item.keywords) {
          if (text.includes(kw)) {
            const paper = PAPER_TYPES[item.id];
            return {
              id: item.id, name: paper ? paper.name : kw, matched: kw,
              confidence: 1.0, type: item.type,
              lengthPerSheet: paper ? paper.lengthPerSheet : 0
            };
          }
        }
      }
      let best = null;
      let bestScore = 0;
      for (const pid in PAPER_TYPES) {
        const paper = PAPER_TYPES[pid];
        const score = fuzzyMatchScore(text, paper.name);
        if (score > bestScore) {
          bestScore = score;
          best = { id: pid, name: paper.name, confidence: score, type: paper.type, lengthPerSheet: paper.lengthPerSheet };
        }
        for (const kw of paper.keywords || []) {
          const kwScore = fuzzyMatchScore(text, kw);
          if (kwScore > bestScore) {
            bestScore = kwScore;
            best = { id: pid, name: paper.name, matched: kw, confidence: kwScore, type: paper.type, lengthPerSheet: paper.lengthPerSheet };
          }
        }
      }
      return best && bestScore > 0.5 ? best : null;
    },

    extractQuantity(text) {
      if (!text) return null;
      const regex = /(\d+|[一二两三四五六七八九十百千]+)\s*(张|卷|米|尺|开|幅|页)/g;
      const matches = [...text.matchAll(regex)];
      if (matches.length === 0) return null;
      const m = matches[0];
      const num = chineseToNumber(m[1]);
      const unit = m[2];
      return { raw: m[0], number: num, unit: unit, confidence: 1.0 };
    },

    extractFont(text) {
      if (!text) return null;
      for (const font of FONT_KEYWORDS) {
        if (text.includes(font)) return { font: font, confidence: 1.0 };
      }
      return null;
    },

    extractCopybook(text) {
      if (!text) return null;
      let best = null;
      let bestScore = 0;
      for (const book of COPYBOOK_LIST) {
        const bookName = book.name || book.copybookName || '';
        const score = fuzzyMatchScore(text, bookName);
        if (score > bestScore) {
          bestScore = score;
          best = book;
        }
      }
      if (best && bestScore > 0.5) {
        return {
          id: best.copybookId || best.id, name: best.name || best.copybookName,
          fontId: best.fontId, fontName: best.fontName,
          authorId: best.authorId, authorName: best.authorName, confidence: bestScore
        };
      }
      return null;
    },

    extractStatus(text, paperType) {
      if (!text) return paperType === 'scroll' ? 'started' : 'completed';
      if (/开了|开始|新.*卷|起卷|新开/.test(text)) return 'started';
      if (/继续|又写|再写|追加|再加/.test(text)) return 'ongoing';
      if (/完成|写完|结束|好了|搞定/.test(text)) return 'completed';
      return paperType === 'scroll' ? 'started' : 'completed';
    },

    calculateMeters(quantity, lengthPerSheet) {
      if (!quantity || !lengthPerSheet) return 0;
      return +(quantity.number * lengthPerSheet).toFixed(2);
    },

    calculateConfidence(results) {
      let score = 0;
      let count = 0;
      if (results.paper) { score += results.paper.confidence; count++; }
      if (results.quantity) { score += 1.0; count++; }
      if (results.copybook) { score += results.copybook.confidence; count++; }
      if (results.font) { score += results.font.confidence; count++; }
      return count > 0 ? +(score / count).toFixed(2) : 0;
    },

    parseInput(text) {
      if (!text || text.trim().length === 0) {
        return { confidence: 0, rawText: text };
      }
      const trimmed = text.trim();
      const paper = this.extractPaper(trimmed);
      const quantity = this.extractQuantity(trimmed);
      const font = this.extractFont(trimmed);
      const copybook = this.extractCopybook(trimmed);
      const paperType = paper ? paper.type : (quantity && quantity.unit === '米' ? 'scroll' : 'sheet');
      const status = this.extractStatus(trimmed, paperType);
      const meters = paper ? this.calculateMeters(quantity, paper.lengthPerSheet) : 0;
      const results = { paper, quantity, font, copybook, status, meters, rawText: trimmed };
      results.confidence = this.calculateConfidence(results);
      return results;
    }
  };

  window.SHUFA_PARSER = parser;
})();
