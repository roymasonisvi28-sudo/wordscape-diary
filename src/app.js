(function () {
  "use strict";
  const DATA = window.GAME_DATA;
  const KEY = "wordscape-diary-save-v1";
  const BANANA_WORDS = [
    ["perspicacious", "有敏锐洞察力的"], ["obfuscate", "使模糊；使困惑"], ["intransigent", "不妥协的；强硬的"],
    ["ephemeral", "短暂的；转瞬即逝的"], ["ubiquitous", "无处不在的"], ["ameliorate", "改善；缓和"],
    ["equivocal", "模棱两可的"], ["fastidious", "挑剔的；讲究的"], ["magnanimous", "宽宏大量的"],
    ["recalcitrant", "顽抗的；难以驾驭的"], ["surreptitious", "秘密进行的；鬼鬼祟祟的"], ["vicissitude", "变迁；人生起伏"],
  ].map(([word, meaning], index) => ({ id: index + 1, word, meaning }));
  const defaultState = () => ({
    chapter: 1, unlocked: 1, checkpoint: null, streak: 1, lastStudy: "", mastered: {}, wrong: {}, learned: {},
    characters: Object.fromEntries(DATA.characters.map(c => [c.id, { affection: 0, trust: 0, resonance: 0, events: [] }])),
    banana: { affection: 0, wrong: 0, encounters: 0, checkedChapters: {} },
    settings: { textSpeed: 22, autoSpeed: 1500, theme: "light", bgm: true, bgmVolume: 0.34 },
    bestScore: 0, route: "su"
  });
  let state = load();
  let view = "home", currentChapter = null, line = 0, choiceRound = 0, typingTimer = null, autoTimer = null, fast = false, auto = false, session = null;
  const app = document.getElementById("app");
  const bgm = new Audio();
  bgm.innerHTML = `<source src="assets/audio/heavenly-loop.ogg" type="audio/ogg"><source src="assets/audio/calm-loop.mp3" type="audio/mpeg">`;
  bgm.loop = true; bgm.preload = "auto";
  function load() { try { const base = defaultState(), stored = JSON.parse(localStorage.getItem(KEY) || "{}"), merged = Object.assign(base, stored, { settings: Object.assign(base.settings, stored.settings || {}), banana: Object.assign(base.banana, stored.banana || {}) }); if (!stored.checkpoint && merged.unlocked > merged.chapter) merged.chapter = merged.unlocked; return merged; } catch (_) { return defaultState(); } }
  function store() { localStorage.setItem(KEY, JSON.stringify(state)); }
  function save() { store(); toast("进度已保存"); }
  function syncBgm() { bgm.volume = Number(state.settings.bgmVolume ?? .34); if (state.settings.bgm) bgm.play().catch(() => {}); else bgm.pause(); }
  function h(tag, cls, html) { return `<${tag}${cls ? ` class="${cls}"` : ""}>${html}</${tag}>`; }
  function rel(v) { return ["普通同学","一起学习","被她注意","特别关心","暧昧未明","心意确认"][Math.min(5, Math.floor(v / 18))]; }
  function nav() { return `<nav><button data-go="home">首页</button><button data-go="daily">每日学习</button><button data-go="memory">记忆回廊</button><button data-go="characters">角色档案</button><button data-go="stats">学习统计</button><button data-go="settings">设置</button></nav>`; }
  function shell(content) { app.innerHTML = `<main class="shell">${content}</main>${nav()}<div id="toast"></div>`; bindNav(); }
  function bindNav() { document.querySelectorAll("[data-go]").forEach(b => b.onclick = () => render(b.dataset.go)); }
  function toast(text) { const el = document.getElementById("toast"); if (!el) return; el.textContent = text; el.classList.add("show"); setTimeout(() => el.classList.remove("show"), 1300); }
  function render(next = view) {
    clearTimers(); view = next;
    if (state.banana.affection >= 50) return bananaConfession();
    ({home, characters, memory, stats, settings, daily, chapters}[view] || home)();
  }
  function home() {
    const learned = Object.keys(state.learned).length;
    shell(`<section class="hero"><div><p class="eyebrow">佳瑞英语社</p><h1>词境恋习日记</h1><p>在一次次并肩自习里，把陌生单词写进记忆，也写进属于你的校园故事。</p><div class="actions"><button class="primary" id="continue">继续游戏</button><button id="new">新的开始</button><button data-go="daily">今日学习</button></div></div><div class="hero-card"><span>今日问候</span><strong>${DATA.characters[state.chapter % 3].name}</strong><p>${DATA.characters[state.chapter % 3].greeting}</p></div></section>
    <section class="dashboard"><article><b>${learned}</b><span>已接触单词</span></article><article><b>${Object.keys(state.wrong).length}</b><span>记忆回廊</span></article><article><b>${state.streak}</b><span>连续学习天数</span></article><article><b>${state.unlocked}/33</b><span>已解锁章节</span></article></section>
    <section><div class="section-title"><h2>最近的约定</h2><button data-go="chapters">章节列表</button></div>${characterCards(true)}</section>`);
    bindNav(); document.getElementById("continue").onclick = resumeGame;
    document.getElementById("new").onclick = () => { if (confirm("确认从头开始？现有进度会被覆盖。")) { state = defaultState(); save(); render(); } };
  }
  function characterStem(id) { return ({ lin: "lin-zhixia", su: "su-wanqing", tang: "tang-xiaoman" })[id]; }
  function characterImage(id) { return `assets/characters/${characterStem(id)}-normal.png?v=4`; }
  function expressionImage(id, expression) { return `assets/characters/${characterStem(id)}-${expression}.png?v=4`; }
  function characterCards(compact = false) { return `<div class="cards">${DATA.characters.map(c => { const s = state.characters[c.id]; return `<article class="character-card" style="--accent:${c.color}"><div class="portrait ${c.id}"><img src="${characterImage(c.id)}" alt="${c.name}上半身立绘"></div><div><small>${c.identity}</small><h3>${c.name}<em>${c.age} 岁</em></h3><p>${compact ? c.personality : c.arc}</p><label>心动值 <b>${s.affection}</b> · ${rel(s.affection)}</label><div class="meter"><i style="width:${Math.min(100,s.affection)}%"></i></div>${compact ? "" : `<p class="meta">信任 ${s.trust} · 共鸣 ${s.resonance}<br>主题：${c.theme}</p>`}</div></article>`; }).join("")}</div>`; }
  function characters() { shell(`<header><p class="eyebrow">CHARACTER ARCHIVE</p><h1>角色档案</h1><p>她们有自己的目标，也会在共同学习中慢慢改变。</p></header>${characterCards()}`); }
  function chapters() { shell(`<header><p class="eyebrow">STORY MAP</p><h1>章节列表</h1><p>原型共 33 章。每章拥有独立校园事件，三条个人线会随着复习约定逐步推进。</p></header><div class="chapter-grid">${DATA.chapters.map(c => `<button class="chapter ${c.id <= state.unlocked ? "" : "locked"}" data-chapter="${c.id}" ${c.id > state.unlocked ? "disabled" : ""}><b>${String(c.id).padStart(2,"0")}</b><span>${c.title}</span><small>${c.scene}</small></button>`).join("")}</div>`); document.querySelectorAll("[data-chapter]").forEach(b => b.onclick = () => startChapter(+b.dataset.chapter)); }
  function startChapter(id) { currentChapter = DATA.chapters[id - 1]; state.chapter = id; line = 0; choiceRound = 0; state.checkpoint = { chapter: id, stage: "story", line: 0, choiceRound: 0 }; store(); story(); }
  function resumeGame() {
    const checkpoint = state.checkpoint;
    if (!checkpoint || checkpoint.chapter !== state.chapter) return startChapter(state.chapter);
    currentChapter = DATA.chapters[checkpoint.chapter - 1]; line = checkpoint.line || 0; choiceRound = checkpoint.choiceRound || 0;
    if (checkpoint.stage === "choice") return choice();
    if (checkpoint.stage === "challenge") return startChallenge(currentChapter.word_ids);
    story();
  }
  function story() {
    view = "story"; const c = currentChapter, d = c.dialogue[line], heroine = DATA.characters.find(x => x.id === c.character);
    app.innerHTML = `<main class="story bg-${sceneClass(c.scene)}"><div class="story-top"><button data-go="chapters">← 章节</button><span>${c.title}</span><div><button id="fast">${fast ? "快进中" : "快进"}</button><button id="auto">${auto ? "自动中" : "自动"}</button></div></div>${heroine ? `<div class="sprite ${heroine.id} expression-${d.expression}"><img src="${expressionImage(heroine.id, d.expression)}" onerror="this.onerror=null;this.src='${characterImage(heroine.id)}'" alt="${heroine.name}${d.expression}表情上半身立绘"><span>${d.expression}</span></div>` : ""}<section class="dialogue"><b>${d.speaker}</b><p id="line"></p><small>点击对话框继续</small></section></main><div id="toast"></div>`;
    bindNav(); typeText(d.text); document.querySelector(".dialogue").onclick = nextLine;
    document.getElementById("fast").onclick = () => { fast = !fast; story(); };
    document.getElementById("auto").onclick = () => { auto = !auto; story(); };
    if (auto) autoTimer = setTimeout(nextLine, state.settings.autoSpeed);
  }
  function typeText(text) { const el = document.getElementById("line"); let i = 0; clearInterval(typingTimer); if (fast) return el.textContent = text; typingTimer = setInterval(() => { el.textContent = text.slice(0, ++i); if (i >= text.length) clearInterval(typingTimer); }, state.settings.textSpeed); }
  function nextLine() { clearTimers(); if (++line < currentChapter.dialogue.length) { state.checkpoint = { chapter: currentChapter.id, stage: "story", line, choiceRound: 0 }; store(); if (line === 2 && maybeBananaEncounter()) return; return story(); } choice(); }
  function maybeBananaEncounter() {
    if (!currentChapter || state.banana.checkedChapters[currentChapter.id]) return false;
    state.banana.checkedChapters[currentChapter.id] = true; store();
    if (Math.random() > .78) return false;
    bananaQuestion(); return true;
  }
  function bananaImage() { return "assets/characters/banana-kun.jpg?v=1"; }
  function bananaQuestion() {
    const word = BANANA_WORDS[Math.floor(Math.random() * BANANA_WORDS.length)];
    const pool = [word, ...BANANA_WORDS.filter(item => item.id !== word.id).sort(() => Math.random() - .5).slice(0, 3)].sort(() => Math.random() - .5);
    state.banana.encounters++; store();
    app.innerHTML = `<main class="banana-event"><div class="banana-card"><img src="${bananaImage()}" alt="香蕉君"><p class="eyebrow">神秘乱入 · 超纲突击</p><h1>香蕉君</h1><p>嘿，先别急着和她聊天。答对这题，我就识趣地消失。</p><h2><strong>${word.word}</strong> 是什么意思？</h2><div class="options">${pool.map(item => `<button data-banana-answer="${item.id}">${item.meaning}</button>`).join("")}</div><small>香蕉君好感 ${state.banana.affection}/50 · 答错会让他更来劲</small></div></main>`;
    document.querySelectorAll("[data-banana-answer]").forEach(button => button.onclick = () => answerBanana(+button.dataset.bananaAnswer, word));
  }
  function answerBanana(id, word) {
    const ok = id === word.id;
    if (ok) state.banana.affection = Math.max(0, state.banana.affection - 1);
    else { state.banana.wrong++; state.banana.affection = Math.min(50, state.banana.affection + 1); }
    store();
    if (state.banana.affection >= 50) return bananaConfession();
    if (ok) return bananaExit("居然答对了。行吧，这次先把时间还给你们。");
    bananaTakeover(word);
  }
  function bananaExit(message) {
    app.innerHTML = `<main class="banana-event banana-exit"><div class="banana-card"><img src="${bananaImage()}" alt="香蕉君"><h1>香蕉君</h1><p>${message}</p><button class="primary" id="banana-back">继续刚才的剧情</button></div></main>`;
    document.getElementById("banana-back").onclick = story;
  }
  function bananaTakeover(word) {
    app.innerHTML = `<main class="banana-takeover"><img src="${bananaImage()}" alt="香蕉君占领屏幕"><div><h1>香蕉君占领了屏幕</h1><p><strong>${word.word}</strong> 没答对。他开心地挡住了你和她的对话。</p><b id="banana-countdown">5</b></div></main>`;
    let seconds = 5;
    const timer = setInterval(() => { seconds--; const counter = document.getElementById("banana-countdown"); if (counter) counter.textContent = seconds; if (seconds <= 0) { clearInterval(timer); bananaExit("好啦，不逗你了。下次可要答对。"); } }, 1000);
  }
  function bananaConfession() {
    app.innerHTML = `<main class="banana-takeover banana-confession"><img src="${bananaImage()}" alt="香蕉君兴奋告白"><div><p class="eyebrow">隐藏结局 · 香蕉君好感 MAX</p><h1>抓到你了</h1><p>答错五十次还不躲着我，你一定是在等我出现吧？从现在开始，屏幕归我了。</p><button class="primary" id="banana-new-game">开始新的游戏</button></div></main>`;
    document.getElementById("banana-new-game").onclick = () => { if (confirm("确认开始新的游戏？当前进度会被清空。")) { localStorage.removeItem(KEY); state = defaultState(); render("home"); } };
  }
  function choice() { const c = currentChapter, rounds = c.choice_rounds || [c.choices], options = rounds[choiceRound]; state.checkpoint = { chapter: c.id, stage: "choice", line: c.dialogue.length, choiceRound }; store(); app.innerHTML = `<main class="choice bg-${sceneClass(c.scene)}"><section><p class="eyebrow">你的选择 · ${choiceRound + 1}/${rounds.length}</p><h2>这一刻，你会怎么回应？</h2>${options.map((x,i) => `<button data-choice="${i}">${x.text}</button>`).join("")}</section></main><div id="toast"></div>`; document.querySelectorAll("[data-choice]").forEach(b => b.onclick = () => applyChoice(options[+b.dataset.choice])); }
  function applyChoice(selection) { const id = currentChapter.character || "su", s = state.characters[id]; Object.keys(selection.effect).forEach(k => s[k] += selection.effect[k]); state.route = id; const rounds = currentChapter.choice_rounds || [currentChapter.choices]; if (++choiceRound < rounds.length) { save(); return choice(); } state.checkpoint = { chapter: currentChapter.id, stage: "challenge", line: currentChapter.dialogue.length, choiceRound }; save(); startChallenge(currentChapter.word_ids); }
  function startChallenge(ids, memoryMode = false) {
    const words = (ids || []).map(id => DATA.words[id - 1]).filter(Boolean);
    if (!words.length) { toast("本章互动暂未准备好，已返回章节页"); return setTimeout(() => render("chapters"), 900); }
    session = { words, at: 0, correct: 0, combo: 0, maxCombo: 0, memoryMode }; challenge();
  }
  function challengeHost(word) {
    const id = currentChapter?.character || word.related_character_id || state.route || "su";
    return DATA.characters.find(character => character.id === id) || DATA.characters[1];
  }
  function pick(list) { return list[session.at % list.length]; }
  function questionLine(host, word) {
    const lines = {
      lin: [
        `学弟，先别急着翻书。看着我回答：<strong>${word.word}</strong> 是什么意思？`,
        `这个词我昨天才提醒过你。学弟，要是答错了，今晚就别想提前走。<strong>${word.word}</strong> 是什么意思？`,
        `不许偷瞄笔记。学弟，答对 <strong>${word.word}</strong>，我就考虑再夸你一句。`,
      ],
      su: [
        `学弟，今天换我来考考你。答对 <strong>${word.word}</strong>，我就给你一点特别奖励。`,
        `学弟，别紧张。我会一直看着你。<strong>${word.word}</strong> 的中文意思，还记得吗？`,
        `我把这一题特意留给你了。学弟，<strong>${word.word}</strong> 是什么意思？`,
      ],
      tang: [
        `学长，今天轮到我考你啦。<strong>${word.word}</strong> 是什么意思？答对了我就靠近一点告诉你奖励。`,
        `学长，这题答对的话，我会很认真地夸你。<strong>${word.word}</strong> 是什么意思？`,
        `不许偷偷翻错词本哦。学长，答错了就要多陪我一会儿。<strong>${word.word}</strong> 是什么意思？`,
      ],
    };
    return pick(lines[host.id]);
  }
  function answerLine(host, word, ok) {
    const lines = {
      lin: ok ? [
        `答对了。学弟，看来你确实有认真听。……别因为我多看了你一眼就得意。`,
        `不错。这个词我只讲过一次，你居然记住了。今晚的位置，还是留给你。只许坐我旁边。`,
        `还算可以。学弟，你认真看着我的时候……有点让人没办法移开视线。`,
      ] : [
        `又错了。学弟，你不行啊。把 <strong>${word.word}</strong> 圈起来，今晚坐我旁边再过一遍。`,
        `不许躲开。真正记住之前，我会一直问。学弟，这次靠近一点，看我的笔记。`,
      ],
      su: ok ? [
        `答对了，学弟。你好棒。被你这样认真看着，我都快忘了自己还要继续出题。`,
        `嗯，就是这个答案。学弟进步得这么快，我好像可以再依赖你一点。只多一点点。`,
        `学弟真厉害。作为奖励，下次靠窗的位置还是留给你。要坐在我旁边哦。`,
      ] : [
        `你不行啊，学弟。答案是 <strong>${word.word}</strong>。……别露出那种表情，我会陪你慢慢记牢。`,
        `差一点点。学弟，把这个词交给我。下次见面时，我会靠近一点再悄悄问你。`,
      ],
      tang: ok ? [
        `答对啦，学长！你好棒！奖励是我再陪你一会儿，开心吗？`,
        `学长好厉害。那我是不是可以靠近一点得意一下？毕竟是我出的题。`,
        `嘿嘿，学长记住了。那明天也要陪我一起背，不许把时间偷偷留给别人。`,
      ] : [
        `欸，学长不行呀。答案是 <strong>${word.word}</strong>。罚你多陪我复习五分钟，不过分吧？`,
        `学长别皱眉。我也错过好多次。下次换我贴近一点提醒你，约好了。`,
      ],
    };
    return pick(lines[host.id]);
  }
  function challenge() {
    const w = session.words[session.at], host = challengeHost(w), pool = [w, ...DATA.words.filter(x => x.id !== w.id).sort(() => Math.random() - .5).slice(0,3)].sort(() => Math.random() - .5);
    app.innerHTML = `<main class="interaction bg-${sceneClass(currentChapter?.scene || "自习室")}"><div class="interaction-top"><span>${session.memoryMode ? "记忆回廊 · 再次相遇" : `今日的约定 · ${session.at + 1}/${session.words.length}`}</span><b>${host.name}</b></div><div class="interaction-sprite sprite ${host.id} expression-serious"><img src="${expressionImage(host.id, "serious")}" onerror="this.onerror=null;this.src='${characterImage(host.id)}'" alt="${host.name}认真表情上半身立绘"></div><section class="interaction-box"><p class="speaker">${host.name}</p><h2>${questionLine(host, w)}</h2><div class="options">${pool.map(x => `<button data-answer="${x.id}">${x.meaning_cn}</button>`).join("")}</div></section></main><div id="toast"></div>`;
    document.querySelectorAll("[data-answer]").forEach(b => b.onclick = () => answer(+b.dataset.answer, w));
  }
  function answer(id, w) {
    const ok = id === w.id, host = challengeHost(w); state.learned[w.id] = true; state.mastered[w.id] = Math.min(4, (state.mastered[w.id] || 0) + (ok ? 1 : 0));
    if (ok) { session.correct++; session.combo++; delete state.wrong[w.id]; } else { session.combo = 0; state.wrong[w.id] = (state.wrong[w.id] || 0) + 1; }
    const heartbeat = ok;
    if (heartbeat) state.characters[host.id].affection += 1;
    session.maxCombo = Math.max(session.maxCombo, session.combo); save();
    answerScene(host, w, ok);
  }
  function answerScene(host, word, ok) {
    const expression = ok ? (session.combo > 1 ? "shy" : "smile") : "sad";
    app.innerHTML = `<main class="interaction feedback-scene bg-${sceneClass(currentChapter?.scene || "自习室")}"><div class="interaction-top"><span>${ok ? "她似乎很满意" : "她轻轻叹了口气"}</span><b>${host.name}</b></div><div class="interaction-sprite sprite ${host.id} expression-${expression}">${ok ? `<div class="floating-hearts"><i>♥</i><i>♥</i><i>♥</i></div>` : ""}<img src="${expressionImage(host.id, expression)}" onerror="this.onerror=null;this.src='${characterImage(host.id)}'" alt="${host.name}${expression}表情上半身立绘"></div><section class="interaction-box feedback-box"><p class="speaker">${host.name}</p><h2>${answerLine(host, word, ok)}</h2>${ok ? `<p class="heartbeat">心动值 +1 · 她的心情似乎变好了。</p>` : ""}<div class="word-note"><b>${word.word}</b><span>${word.meaning_cn}</span><small>${word.example_en}<br>${word.example_cn}</small></div><button class="primary" id="nextq">${session.at + 1 === session.words.length ? "和她一起看看今天的成果" : "继续陪她复习"}</button></section></main><div id="toast"></div>`;
    document.getElementById("nextq").onclick = () => { if (++session.at < session.words.length) challenge(); else settlement(); };
  }
  function settlement() {
    const score = Math.round(session.correct / session.words.length * 100); state.bestScore = Math.max(score, state.bestScore);
    if (!session.memoryMode && score >= currentChapter.unlock_score) {
      state.unlocked = Math.min(DATA.chapters.length, Math.max(state.unlocked, currentChapter.id + 1));
      state.chapter = Math.min(DATA.chapters.length, currentChapter.id + 1);
      state.checkpoint = null;
    }
    save(); shell(`<section class="result"><p class="eyebrow">STUDY REPORT</p><h1>${score} 分</h1><p>${score >= 80 ? "这一页，已经开始留在你的记忆里了。" : "没关系。错过的词，会在记忆回廊里等你重新遇见。"}</p><div class="dashboard"><article><b>${session.words.length}</b><span>学习单词</span></article><article><b>${session.correct}</b><span>回答正确</span></article><article><b>${session.maxCombo}</b><span>最高连击</span></article></div><div class="actions"><button class="primary" data-go="home">返回首页</button><button data-go="memory">查看记忆回廊</button></div></section>`); bindNav();
  }
  function memory() { const ids = Object.keys(state.wrong).map(Number), words = ids.map(id => DATA.words[id-1]); shell(`<header><p class="eyebrow">MEMORY CORRIDOR</p><h1>记忆回廊</h1><p>答错的词并不是失败，只是下一次相遇的坐标。</p></header>${words.length ? `<button class="primary" id="review">重新挑战 ${Math.min(10,words.length)} 个错词</button><div class="word-list">${words.map(w => `<article><b>${w.word}</b><span>${w.meaning_cn}</span><small>${w.related_character} · 错误 ${state.wrong[w.id]} 次</small></article>`).join("")}</div>` : `<div class="empty">回廊里还没有错词。继续保持。</div>`}`); if (words.length) document.getElementById("review").onclick = () => startChallenge(ids.slice(0,10), true); }
  function stats() { const learned = Object.keys(state.learned).length, mastered = Object.values(state.mastered).filter(x => x >= 2).length; shell(`<header><p class="eyebrow">LEARNING STATS</p><h1>学习统计</h1></header><section class="dashboard"><article><b>${learned}</b><span>接触单词</span></article><article><b>${mastered}</b><span>已掌握</span></article><article><b>${Object.keys(state.wrong).length}</b><span>错词数量</span></article><article><b>${state.bestScore}</b><span>最高分</span></article></section><div class="panel"><h2>词库进度</h2><p>首版核心高频词：500 个</p><div class="meter"><i style="width:${learned/5}%"></i></div><p>基础、提升、高阶三层结构已经保留，可继续扩展至约 2000 词。</p></div>`); }
  function daily() { const day = new Date().toISOString().slice(0,10); if (state.lastStudy !== day) { state.lastStudy = day; state.streak += 1; save(); } const ids = DATA.words.slice((new Date().getDate()*7)%450).slice(0,10).map(x=>x.id); shell(`<header><p class="eyebrow">DAILY STUDY</p><h1>今日学习</h1><p>${DATA.characters[new Date().getDate()%3].greeting}</p></header><div class="panel"><h2>今日推荐</h2><p>10 个新词与错词回顾会计入连续学习天数。</p><button class="primary" id="daily-start">开始今日挑战</button></div>`); document.getElementById("daily-start").onclick=()=>startChallenge(ids,true); }
  function settings() { shell(`<header><p class="eyebrow">SETTINGS</p><h1>设置</h1></header><div class="panel settings"><label>文字速度 <input id="speed" type="range" min="8" max="60" value="${state.settings.textSpeed}"></label><label>自动播放间隔 <input id="autospeed" type="range" min="800" max="3000" step="100" value="${state.settings.autoSpeed}"></label><label><input id="bgm" type="checkbox" ${state.settings.bgm ? "checked":""}> 开启背景音乐</label><label>背景音乐音量 <input id="bgmVolume" type="range" min="0" max="1" step="0.05" value="${state.settings.bgmVolume ?? .34}"></label><label>主题 <select id="theme"><option value="light">浅色</option><option value="dark" ${state.settings.theme==="dark"?"selected":""}>深色</option></select></label><button id="manual">手动存档</button><button class="danger" id="reset">重置进度</button></div>`); document.getElementById("manual").onclick=save; document.getElementById("reset").onclick=()=>{if(confirm("确认删除全部进度？")){localStorage.removeItem(KEY);state=defaultState();render("home");}}; ["speed","autospeed","bgm","bgmVolume","theme"].forEach(id=>document.getElementById(id).onchange=e=>{state.settings[id==="speed"?"textSpeed":id==="autospeed"?"autoSpeed":id]=e.target.type==="checkbox"?e.target.checked:e.target.value; document.body.dataset.theme=state.settings.theme; syncBgm(); save();}); }
  function sceneClass(s) { return ({图书馆:"library",自习室:"study",英语社活动室:"club",咖啡店:"cafe",操场黄昏:"field",雨天校道:"rain",夜晚宿舍窗边:"night",考场:"exam","大学校门":"gate","结局场景":"ending"})[s] || "study"; }
  function clearTimers(){ clearInterval(typingTimer); clearTimeout(autoTimer); }
  document.addEventListener("click", syncBgm, { once: true });
  document.body.dataset.theme = state.settings.theme; render();
})();
