const fs=require("fs"),path=require("path"),root=path.join(__dirname,"..");
const read=n=>JSON.parse(fs.readFileSync(path.join(root,"data",n+".json"),"utf8"));
const words=read("words"),chapters=read("chapters"),characters=read("characters"),specialEvents=read("special-events");
function ok(v,m){if(!v)throw new Error(m)}
ok(words.length===500,"词库应包含 500 词"); ok(chapters.length>=33,"章节数不足"); ok(characters.length===3,"角色数应为 3");
ok(chapters.every(c=>c.dialogue.length>=8),"章节剧情文本不足");
ok(chapters.every(c=>c.choice_rounds.length===3),"每章应包含三轮选择");
ok(specialEvents.length===9,"特别回忆应包含 9 个事件");
ok(characters.every(c=>specialEvents.filter(e=>e.character===c.id).length===3),"每位角色应包含 3 个特别回忆");
["word","phonetic","meaning_cn","meaning_en","example_en","example_cn","difficulty","tags","memory_hint","related_character","scene_usage"].forEach(k=>ok(words.every(w=>w[k]),"缺少字段 "+k));
ok(fs.existsSync(path.join(root,"index.html")),"缺少首页"); console.log("基础数据测试通过：500 词，"+chapters.length+" 章，3 位角色。");
