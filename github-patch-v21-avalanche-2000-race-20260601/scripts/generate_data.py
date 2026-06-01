import csv
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

characters = [
    {
        "id": "lin",
        "name": "林知夏",
        "age": 22,
        "identity": "外国语学院研一学生，考研英语高分选手",
        "personality": "冷静克制，嘴硬心软，习惯用成绩确认努力是否真实。",
        "appearance": "银灰色长直发，灰蓝眼睛，清冷感，银色书签",
        "outfit": "深海军蓝学院风针织外套、灰蓝衬衫、简洁帆布包",
        "color": "#7197d6",
        "theme": "阅读理解与学术表达",
        "vocab": "学术词汇、逻辑连接词、高频抽象词",
        "romance": "竞争、认可、并肩自习、克制的偏心",
        "arc": "从质疑你的基础，到承认你的坚持，再学会不只用分数衡量自己。",
        "events": ["模拟考试后的错题夜谈", "雨天自习室留座", "考场前交换书签"],
        "ending": "她不再把上岸当作唯一答案，与你约定在更长的路上继续并肩。",
        "greeting": "今天的位置给你留着。先说好，迟到一分钟就多背十个词。",
    },
    {
        "id": "su",
        "name": "苏晚晴",
        "age": 23,
        "identity": "英语社社长，新闻传播学院大四学生",
        "personality": "温柔可靠，善于照顾别人，但不太擅长承认自己的疲惫。",
        "appearance": "珊瑚粉色微卷双束长发，暖紫眼睛，温柔笑意，随身便签",
        "outfit": "浅杏粉宽松针织开衫、薄荷绿内搭、茶色半裙",
        "color": "#e6a978",
        "theme": "写作、演讲与情绪表达",
        "vocab": "写作高频词、社交词汇、情绪表达",
        "romance": "陪伴、倾听、互相依靠、靠窗座位",
        "arc": "她先带你走进佳瑞英语社，后来也学会把自己的压力交给你分担。",
        "events": ["英语社迎新演讲", "咖啡店改稿", "深夜窗边语音"],
        "ending": "校级演讲结束后，她坦率说出自己的不安，也接受你的陪伴。",
        "greeting": "今天也来了啊。靠窗的位置很安静，背累了就休息一下。",
    },
    {
        "id": "tang",
        "name": "唐小满",
        "age": 20,
        "identity": "计算机学院大二学生，佳瑞英语社新成员",
        "personality": "活泼直接，偶尔粗心，遇到困难会短暂沮丧但很快重新振作。",
        "appearance": "浅紫银色侧束长发，明亮紫眸，黑色细蝴蝶结，轻盈发梢",
        "outfit": "白色短外套、浅蓝紫翻领、柠檬黄领结、浅蓝半裙",
        "color": "#e3ba55",
        "theme": "基础巩固与易混词辨析",
        "vocab": "基础高频词、校园生活词、易混词",
        "romance": "打卡、错词本、共同成长、元气陪伴",
        "arc": "她从总来求助的学妹，成长为在你状态低落时拉你回到书桌前的人。",
        "events": ["操场黄昏打卡", "错词本交换日", "倒计时互相监督"],
        "ending": "她把写满批注的错词本交给你，笑着说这次换她陪你复习。",
        "greeting": "学长，今天的打卡还没亮！一起背完再去吃饭，好不好？",
    },
]

special_events = [
    {
        "id": "lin-seat", "character": "lin", "threshold": 22, "title": "只留给你的座位", "scene": "图书馆",
        "summary": "闭馆前，她第一次承认每天留座并不是顺便。",
        "dialogue": [
            {"speaker": "旁白", "text": "晚自习开始前，图书馆几乎坐满。你绕到熟悉的窗边，发现林知夏的书旁边仍压着一张写有你名字的便签。", "expression": "normal"},
            {"speaker": "林知夏", "text": "迟到了三分钟。按约定，今晚多背三十个词。", "expression": "serious"},
            {"speaker": "你", "text": "可你还是给我留了位置。林学姐每天都这么顺便吗？", "expression": "normal"},
            {"speaker": "林知夏", "text": "……不是顺便。这里太吵，换别人坐在旁边会影响我。", "expression": "shy"},
            {"speaker": "你", "text": "所以只有我不会影响你？", "expression": "normal"},
            {"speaker": "林知夏", "text": "你会。只是我已经习惯了。学弟，别笑。坐下，陪我到闭馆。", "expression": "shy"},
        ],
    },
    {
        "id": "lin-rain", "character": "lin", "threshold": 48, "title": "伞下的安全距离", "scene": "雨天校道",
        "summary": "一场大雨让她嘴硬地缩短了你们之间的距离。",
        "dialogue": [
            {"speaker": "旁白", "text": "雨点落在伞面上，声音密得像一场突然加速的倒计时。林知夏把伞向你这边偏了偏。", "expression": "normal"},
            {"speaker": "林知夏", "text": "再靠近一点。你的肩膀已经湿了。", "expression": "serious"},
            {"speaker": "你", "text": "林学姐不怕我误会？", "expression": "normal"},
            {"speaker": "林知夏", "text": "你误会得还少吗？现在先听话。", "expression": "jealous"},
            {"speaker": "旁白", "text": "她没有看你，只是指尖悄悄攥紧伞柄。你们的手背偶尔碰到一起，又谁都没有避开。", "expression": "shy"},
            {"speaker": "林知夏", "text": "学弟，雨停之前……就保持这个距离。只是为了不淋湿。", "expression": "shy"},
        ],
    },
    {
        "id": "lin-bookmark", "character": "lin", "threshold": 82, "title": "书签背面的答案", "scene": "考场",
        "summary": "她把一直没说出口的话藏进了银色书签。",
        "dialogue": [
            {"speaker": "旁白", "text": "考场外的风有些凉。林知夏把银色书签放进你掌心，背面比上次多了一行很小的字。", "expression": "normal"},
            {"speaker": "你", "text": "“以后也坐我旁边。”这是新的复习要求？", "expression": "normal"},
            {"speaker": "林知夏", "text": "不是要求。是我希望你答应的事。", "expression": "serious"},
            {"speaker": "你", "text": "如果我想答应得更久一点呢？", "expression": "normal"},
            {"speaker": "林知夏", "text": "那就别只在这里说。考完以后，认真告诉我。", "expression": "shy"},
            {"speaker": "林知夏", "text": "还有，学弟。今天别紧张。我会在出口等你。", "expression": "smile"},
        ],
    },
    {
        "id": "su-window", "character": "su", "threshold": 22, "title": "靠窗位置的偏心", "scene": "图书馆",
        "summary": "你发现学姐的温柔并不是毫无区别地分给所有人。",
        "dialogue": [
            {"speaker": "旁白", "text": "靠窗的位置放着一杯温水。杯底压着便签：给总是假装不累的某位学弟。", "expression": "normal"},
            {"speaker": "苏晚晴", "text": "你来了啊。我还在想，今天要不要把位置让给别人。", "expression": "smile"},
            {"speaker": "你", "text": "学姐真的舍得？", "expression": "normal"},
            {"speaker": "苏晚晴", "text": "不太舍得。所以你最好每天都来，让我不用考虑这种问题。", "expression": "shy"},
            {"speaker": "你", "text": "听起来，我好像得对这个座位负责。", "expression": "normal"},
            {"speaker": "苏晚晴", "text": "嗯。也稍微对等你的人负责一下，好不好？", "expression": "smile"},
        ],
    },
    {
        "id": "su-call", "character": "su", "threshold": 48, "title": "晚安之前不挂断", "scene": "夜晚宿舍窗边",
        "summary": "她在深夜第一次坦率承认，自己也需要你的陪伴。",
        "dialogue": [
            {"speaker": "旁白", "text": "电话另一端传来翻动稿纸的声音。苏晚晴沉默了一会儿，没有像平时那样先问你的复习进度。", "expression": "normal"},
            {"speaker": "苏晚晴", "text": "学弟，今晚能不能先别挂断？我没有什么要紧的事，只是……想听见你还在。", "expression": "sad"},
            {"speaker": "你", "text": "那就不挂。学姐想安静待着也可以。", "expression": "normal"},
            {"speaker": "苏晚晴", "text": "谢谢。平时我总告诉别人可以依赖我，轮到自己却不太会开口。", "expression": "serious"},
            {"speaker": "你", "text": "以后慢慢练习。先从今晚开始。", "expression": "normal"},
            {"speaker": "苏晚晴", "text": "好。那今晚的最后一句不是复习提醒。是晚安，学弟。明天也要来见我。", "expression": "shy"},
        ],
    },
    {
        "id": "su-key", "character": "su", "threshold": 82, "title": "备用钥匙", "scene": "英语社活动室",
        "summary": "她把活动室的备用钥匙和更长久的约定交给你。",
        "dialogue": [
            {"speaker": "旁白", "text": "清晨的活动室还很安静。苏晚晴把备用钥匙放到你掌心，却没有立刻松开手。", "expression": "normal"},
            {"speaker": "苏晚晴", "text": "以前我总是第一个来，最后一个走。现在好像开始期待有人和我一起。", "expression": "smile"},
            {"speaker": "你", "text": "这把钥匙是社员福利，还是学姐的偏心？", "expression": "normal"},
            {"speaker": "苏晚晴", "text": "学弟已经知道答案了，还一定要我说出来吗？", "expression": "shy"},
            {"speaker": "你", "text": "有些答案，想亲耳听到。", "expression": "normal"},
            {"speaker": "苏晚晴", "text": "那考完以后留下来。不是为了活动室，是为了我。", "expression": "shy"},
        ],
    },
    {
        "id": "tang-sticker", "character": "tang", "threshold": 22, "title": "贴在你书上的星星", "scene": "英语社活动室",
        "summary": "她把每日打卡的第一颗星星郑重贴给了你。",
        "dialogue": [
            {"speaker": "旁白", "text": "唐小满把一张金色星星贴纸按在你的词汇书封面上，认真地抚平翘起的边角。", "expression": "normal"},
            {"speaker": "唐小满", "text": "学长，这是今天的奖励。只发给坚持打卡，而且陪我一起背词的人。", "expression": "smile"},
            {"speaker": "你", "text": "听起来名额只有一个？", "expression": "normal"},
            {"speaker": "唐小满", "text": "本来就只有一个。学长不许拿去跟别人炫耀。", "expression": "jealous"},
            {"speaker": "你", "text": "那我藏好。", "expression": "normal"},
            {"speaker": "唐小满", "text": "也不用藏得太好啦。至少每天翻书的时候，要想起我一次。", "expression": "shy"},
        ],
    },
    {
        "id": "tang-earphone", "character": "tang", "threshold": 48, "title": "耳机线的长度", "scene": "咖啡店",
        "summary": "共享耳机让她找到了一个靠近你的正当理由。",
        "dialogue": [
            {"speaker": "旁白", "text": "咖啡店里有些吵。唐小满把一只耳机递给你，短短的耳机线把你们之间的距离拉近。", "expression": "normal"},
            {"speaker": "唐小满", "text": "学长，再靠近一点点。不然耳机会掉。", "expression": "shy"},
            {"speaker": "你", "text": "真的只是耳机线太短？", "expression": "normal"},
            {"speaker": "唐小满", "text": "当然啦。不然还能是什么？", "expression": "jealous"},
            {"speaker": "旁白", "text": "她嘴上回答得很快，视线却落在桌角。片刻后，她悄悄把音量调小了一格。", "expression": "shy"},
            {"speaker": "唐小满", "text": "这样就可以多听一会儿。学长也不许先把耳机摘掉。", "expression": "smile"},
        ],
    },
    {
        "id": "tang-last-page", "character": "tang", "threshold": 82, "title": "错词本最后一页", "scene": "结局场景",
        "summary": "最后一页写的不是单词，而是她想和你继续的未来。",
        "dialogue": [
            {"speaker": "旁白", "text": "唐小满把厚厚的错词本递给你。最后一页没有单词，只有一行被她反复描过的字。", "expression": "normal"},
            {"speaker": "你", "text": "“考试结束后，也要继续见面。”这算新的打卡任务？", "expression": "normal"},
            {"speaker": "唐小满", "text": "嗯，而且是长期任务。学长不能只坚持到考试结束。", "expression": "serious"},
            {"speaker": "你", "text": "如果我打算一直打卡呢？", "expression": "normal"},
            {"speaker": "唐小满", "text": "那我就一直检查。每天都检查。", "expression": "shy"},
            {"speaker": "唐小满", "text": "学长，说好了哦。以后开心或者不开心，都要留一个位置给我。", "expression": "smile"},
        ],
    },
]

handmade = {
    "abandon": ("放弃；抛弃", "to leave something or stop doing it", "He decided not to abandon his dream.", "他决定不放弃自己的梦想。", "重要的目标不该轻易 abandon。"),
    "ability": ("能力；才能", "the power or skill to do something", "Practice improves your ability to read quickly.", "练习会提升你的快速阅读能力。", "她在成绩单旁写下：ability 也来自日复一日。"),
    "achieve": ("实现；达到", "to succeed in reaching a goal", "Small steps help us achieve a difficult goal.", "小步前进帮助我们实现困难的目标。", "你们约定一起 achieve 下一次模拟考目标。"),
    "analyze": ("分析", "to examine something carefully", "She asked you to analyze the structure of the passage.", "她让你分析文章结构。", "林知夏把笔递来：先 analyze，再做选择。"),
    "encourage": ("鼓励", "to give someone support or confidence", "Her note encouraged you to continue studying.", "她的便签鼓励你继续学习。", "苏晚晴的便签总能 encourage 你再坚持一会儿。"),
    "persist": ("坚持", "to continue despite difficulty", "If you persist, the unfamiliar words will become easier.", "如果你坚持，陌生词会变得容易。", "小满认真地说：我们一起 persist 到最后。"),
    "significant": ("重要的；显著的", "important or large enough to be noticed", "Daily review makes a significant difference.", "每日复习会带来显著改变。", "你的正确率出现了 significant 的变化。"),
    "approach": ("方法；接近", "a way of dealing with something; to move nearer", "Try a different approach to this question.", "试试用不同的方法解这道题。", "她在草稿纸上圈出 approach：方法比硬撑更重要。"),
    "contribute": ("贡献；促成", "to help cause or produce something", "Regular sleep can contribute to better memory.", "规律睡眠有助于提高记忆力。", "每次复习都 contribute to 最后的上岸。"),
    "contrast": ("对比；形成对照", "a clear difference between things", "The contrast between the two options is subtle.", "两个选项之间的差别很细微。", "她让你 contrast 两个易混词，再决定答案。"),
    "essential": ("必要的；本质的", "completely necessary or extremely important", "Review is essential for long-term memory.", "复习对长期记忆至关重要。", "苏晚晴轻声提醒：休息也是 essential 的。"),
    "motivate": ("激励；促使", "to make someone want to act", "A clear plan can motivate you to study.", "清晰的计划能激励你学习。", "你发现，约定比闹钟更能 motivate 自己。"),
}

def clean_translation(text):
    text = (text or "").split("\\n")[0].strip()
    text = text.replace("vt.", "").replace("vi.", "").replace("n.", "").replace("a.", "").replace("ad.", "")
    return text[:60] or "常用英语词汇"

def load_words():
    rows = []
    with open(ROOT / ".cache" / "ecdict.csv", encoding="utf-8", newline="") as fh:
        for row in csv.DictReader(fh):
            word = row["word"].strip()
            tags = (row.get("tag") or "").split()
            if "ky" not in tags or "cet4" not in tags or not word.isalpha() or len(word) < 3:
                continue
            freq = int(row.get("frq") or 0) or 999999
            bnc = int(row.get("bnc") or 0) or 999999
            rows.append((min(freq, bnc), word.lower(), row))
    rows.sort(key=lambda item: (item[0], item[1]))
    selected = []
    seen = set()
    for _, word, row in rows:
        if word in seen:
            continue
        seen.add(word)
        selected.append((word, row))
        if len(selected) == 500:
            break
    result = []
    for index, (word, row) in enumerate(selected, 1):
        tier = "基础" if index <= 220 else "中等" if index <= 400 else "困难"
        char = characters[(index - 1) % 3]
        meaning = clean_translation(row.get("translation"))
        definition = (row.get("definition") or "").split("\\n")[0].strip()[:180]
        if word in handmade:
            meaning, definition, example_en, example_cn, usage = handmade[word]
        else:
            example_en = f'The study group reviewed the word "{word}" in context.'
            example_cn = f'学习小组结合语境复习了单词“{word}”。'
            usage = f'{char["name"]}在你的卡片上写下 {word}，提醒你把它放回复习队列。'
        result.append({
            "id": index, "word": word, "phonetic": f'/{row.get("phonetic") or ""}/',
            "pos": (row.get("pos") or "常用词").split("/")[0],
            "meaning_cn": meaning, "meaning_en": definition or f"a commonly used English word related to {meaning}",
            "example_en": example_en, "example_cn": example_cn, "difficulty": tier,
            "tags": ["考研核心", "高频", "ECDICT-ky", char["vocab"].split("、")[0]],
            "memory_hint": f"先记住核心义“{meaning.split('，')[0]}”，再在例句中复现。",
            "related_character": char["name"], "related_character_id": char["id"],
            "scene_usage": usage,
        })
    return result

def load_avalanche_words():
    rows = []
    with open(ROOT / ".cache" / "ecdict.csv", encoding="utf-8", newline="") as fh:
        for row in csv.DictReader(fh):
            word = row["word"].strip()
            tags = (row.get("tag") or "").split()
            if "ky" not in tags or not word.isalpha() or len(word) < 3:
                continue
            freq = int(row.get("frq") or 0) or 999999
            bnc = int(row.get("bnc") or 0) or 999999
            rows.append((min(freq, bnc), word.lower(), row))
    rows.sort(key=lambda item: (item[0], item[1]))
    result, seen = [], set()
    for _, word, row in rows:
        if word in seen:
            continue
        seen.add(word)
        result.append({"id": len(result) + 1, "word": word, "meaning_cn": clean_translation(row.get("translation"))})
        if len(result) == 2000:
            break
    return result

def build_chapters(words):
    beats = [
        ("序章 01：掉在及格线外", "分班测试失败", "大学校门", "su", "分班测试成绩单",
         "分班测试的成绩贴在公告栏上。你站在人群最后，那个没有及格的分数格外醒目。",
         "苏晚晴", "学弟，要不要先别急着把成绩单揉掉？承认这次没考好，不等于承认自己不行。",
         "你", "被学姐撞见这种场面，还真有点狼狈。",
         "苏晚晴", "那就把狼狈留在今天吧。明天来英语社，我给你留一个位置。"),
        ("序章 02：佳瑞英语社", "加入佳瑞英语社", "英语社活动室", "su", "英语社报名表",
         "活动室里有淡淡的咖啡香。苏晚晴把报名表推到你面前，指尖压着纸角，没有催促。",
         "苏晚晴", "学弟，签名前可以反悔。不过签下之后，我会认真催你来打卡。",
         "你", "听起来像是被学姐盯上了。",
         "苏晚晴", "是啊。至少在你真正进步以前，我暂时不打算放过你。"),
        ("序章 03：第一次并肩", "第一次单词挑战", "自习室", "lin", "第一次十词约定",
         "夜色落在自习室玻璃上。林知夏把一张十词清单推来，唐小满抱着错词本坐在另一侧。",
         "林知夏", "学弟，基础差不可怕。可怕的是连十个词都不肯认真面对。先看着我，把这十个答完。",
         "你", "那就从这十个开始。至少别让你第一天就看扁我。",
         "林知夏", "口气倒是不小。答得好，我会考虑明天继续坐这里。"),

        ("林知夏线 01：错题本边缘", "错题本上的批注", "图书馆", "lin", "借走错题本",
         "你在图书馆找到自己的错题本时，页边已经多了几行清晰的蓝色批注。",
         "林知夏", "别误会。我只是看不下去有人在同一个地方连续摔三次。",
         "你", "所以你特地帮我改到闭馆？",
         "林知夏", "学弟，少自作多情。真想谢我，就先把我圈出的词答对。答得好，我可以再陪你一会儿。"),
        ("林知夏线 02：无声的较量", "自习室排名", "自习室", "lin", "模拟题赌约",
         "午后的自习室很安静。林知夏把两份模拟题并排放好，在你的分数旁轻轻点了一下。",
         "林知夏", "比上次高了十二分。勉强值得我把你当作对手。",
         "你", "只是对手？我还以为已经能算固定同桌了。",
         "林知夏", "先赢过我一次再说。赢了的话，明天的位置让你选。"),
        ("林知夏线 03：雨天留座", "雨天送伞", "雨天校道", "lin", "共撑一把伞",
         "雨下得突然。教学楼门口，林知夏抱着两本书站在伞下，像是已经等了一会儿。",
         "林知夏", "学弟，你再不过来，我就真的不等了。……伞不大，靠近一点。",
         "你", "原来你是在等我。",
         "林知夏", "……只是顺路。靠近一点，淋湿了会影响今晚的复习效率。"),
        ("林知夏线 04：阅读理解之夜", "闭馆前的并肩", "图书馆", "lin", "闭馆铃声",
         "闭馆广播响起时，你们还在为一篇阅读的转折句争论。林知夏没有收书，只把笔递给你。",
         "林知夏", "学弟，再给你最后一次机会。找出 however 后面真正的重点。",
         "你", "如果答对了，能不能别总把我当普通学弟训？",
         "林知夏", "可以考虑。前提是你别在这种时候故意让我分心。"),
        ("林知夏线 05：模拟考前夕", "操场散步", "操场黄昏", "lin", "放慢十分钟",
         "模拟考前夕，林知夏罕见地没有留在图书馆。夕阳把操场边的影子拉得很长。",
         "林知夏", "我知道你想多做一套题。但学弟，偶尔陪我走十分钟，不算逃避。",
         "你", "这算学霸的特别许可？",
         "林知夏", "只对你有效。明天别让我失望，也别让自己失望。"),
        ("林知夏线 06：并肩的距离", "深夜消息", "夜晚宿舍窗边", "lin", "未发送的关心",
         "深夜十一点，你收到林知夏发来的错题照片。几秒后，又多了一句很快被撤回的消息。",
         "林知夏", "刚才那句不用管。我只是确认你没有熬夜到太晚。",
         "你", "已经看见了。你说的是：累了就早点睡。",
         "林知夏", "……看见就看见。今晚答完这组词，必须休息。"),
        ("林知夏线 07：交换书签", "书签背面的字", "图书馆", "lin", "银色书签",
         "林知夏把常用的银色书签夹进你的词汇书。背面有一行很小的字：不要在终点前怀疑自己。",
         "林知夏", "只是暂时借你。考完要还。",
         "你", "如果舍不得还呢？",
         "林知夏", "那就用另一件东西来换。至于是什么，等你上岸再想。"),
        ("林知夏线 08：考场门口", "克制的偏心", "考场", "lin", "考场前的约定",
         "进考场前，人群从身边匆匆经过。林知夏替你理正书签露出的一角，动作很轻。",
         "林知夏", "学弟，最后一次提醒：别慌。你已经不是第一次见面时的水平了。",
         "你", "考完以后，还能继续坐你旁边吗？",
         "林知夏", "……位置一直给你留着。只是以后，不许再装作不知道。"),

        ("苏晚晴线 01：靠窗的位置", "固定座位", "图书馆", "su", "靠窗座位",
         "你推开图书馆侧门时，靠窗桌上放着一杯温水，旁边还有苏晚晴写好的复习计划。",
         "苏晚晴", "学弟，今天也来了。这个位置光线好，我猜你会喜欢。",
         "你", "学姐是不是对每个社员都这么照顾？",
         "苏晚晴", "你可以先认真背词。等你答对了，我再考虑要不要告诉你答案。"),
        ("苏晚晴线 02：迎新演讲", "后台排练", "英语社活动室", "su", "演讲稿最后一段",
         "迎新活动开始前，苏晚晴独自在空教室里改稿。她念到最后一段时停了两次。",
         "苏晚晴", "学弟，能帮我听一遍吗？平时总是我给别人建议，轮到自己反而有点没底。",
         "你", "原来学姐也会紧张。",
         "苏晚晴", "会啊。所以今天，能不能让我稍微依赖你一下？"),
        ("苏晚晴线 03：咖啡店改稿", "一杯热拿铁", "咖啡店", "su", "咖啡店改稿",
         "窗外的雨声很轻。苏晚晴在咖啡店桌边改你的作文，红笔停在结尾处，没有立刻落下。",
         "苏晚晴", "学弟，这一段写得比以前真诚。只是结尾还差一点勇气。",
         "你", "学姐陪我改到这么晚，我好像更有勇气了。",
         "苏晚晴", "……那我是不是该坐近一点，免得你又把勇气弄丢？"),
        ("苏晚晴线 04：社长的疲惫", "空教室里的沉默", "英语社活动室", "su", "替她收拾资料",
         "活动结束后，苏晚晴仍坐在空教室里。桌上是经费表、报名表和没来得及喝完的冷咖啡。",
         "苏晚晴", "我没事，只是稍微有点累。学弟不用为了我耽误复习。",
         "你", "学姐总说可以依赖别人，自己却不太会。",
         "苏晚晴", "被你发现了啊。那今晚，陪我把资料收完再走，好吗？"),
        ("苏晚晴线 05：夜晚窗边", "迟到的晚安", "夜晚宿舍窗边", "su", "深夜通话",
         "熄灯前，苏晚晴发来一条很短的消息：还醒着吗。你拨过去时，她在电话另一端安静了几秒。",
         "苏晚晴", "学弟，今天不用背太多。我只是想听听你的声音，确认你没有勉强自己。",
         "你", "也确认一下学姐没有勉强自己。",
         "苏晚晴", "嗯。那我们各背五个词，然后认真说晚安。"),
        ("苏晚晴线 06：校级演讲", "舞台侧幕", "英语社活动室", "su", "上台前握手",
         "校级演讲前，苏晚晴站在侧幕阴影里。她向你伸出手，指尖比平时凉一点。",
         "苏晚晴", "学弟，借我一点勇气。只到演讲结束就还你。",
         "你", "不用急着还。可以多借一会儿。",
         "苏晚晴", "那你要负责等我下台。第一眼，我想看见你。"),
        ("苏晚晴线 07：坦率的停顿", "演讲后的长椅", "操场黄昏", "su", "不再逞强",
         "掌声散去后，苏晚晴没有回活动室。她坐在操场边的长椅上，终于慢慢呼出一口气。",
         "苏晚晴", "学弟，我以前以为自己必须一直可靠。可在你面前，好像不用那么努力装作没事。",
         "你", "那就把累的时候也交给我。",
         "苏晚晴", "好。只是这样一来，我可能会越来越舍不得你离开。"),
        ("苏晚晴线 08：约定之后", "社团钥匙", "结局场景", "su", "钥匙与告白",
         "清晨的活动室还没有其他人。苏晚晴把备用钥匙放进你掌心，目光温柔却没有躲开。",
         "苏晚晴", "学弟，佳瑞英语社以后也需要你。不是作为临时来复习的人。",
         "你", "那作为一直陪在学姐身边的人呢？",
         "苏晚晴", "……这个位置，我从很早以前就替你留好了。"),

        ("唐小满线 01：学妹的错词本", "写满贴纸的本子", "英语社活动室", "tang", "交换错词本",
         "唐小满抱着一本贴满彩色便签的错词本冲进活动室，在你桌边急刹车。",
         "唐小满", "学长，救命。我明明昨天记住了，今天它们又像第一次见我。",
         "你", "先把最容易错的十个交出来。",
         "唐小满", "好！不过学长也要给我看你的错词本。共同进步，不许只检查我。"),
        ("唐小满线 02：操场打卡", "黄昏十词挑战", "操场黄昏", "tang", "操场边打卡",
         "晚饭前，唐小满在操场边拦住你，举起手机上的打卡页面，笑得很有底气。",
         "唐小满", "学长，今天的格子还没亮。背完十个词才能放你走。",
         "你", "学妹现在管得这么严格？",
         "唐小满", "因为学长答应过要陪我。说过的话，当然要算数。"),
        ("唐小满线 03：易混词警报", "差一个字母", "自习室", "tang", "易混词便利贴",
         "自习室桌面上排着一串便利贴。唐小满把几个易混词写得特别大，神情难得严肃。",
         "唐小满", "学长，我这次真的要记住。不能每次都靠你提醒。",
         "你", "那我负责出题，答错就加练。",
         "唐小满", "可以。不过答对的话，学长也要认真夸我。"),
        ("唐小满线 04：一起补课", "咖啡店角落", "咖啡店", "tang", "共享耳机",
         "咖啡店里有些吵。唐小满把一只耳机递给你，里面循环播放着她录下的单词清单。",
         "唐小满", "学长，我自己录的。虽然有几个音可能不太准，你不许笑。",
         "你", "那我听完再帮你改。",
         "唐小满", "嗯。耳机线有点短，学长再靠近一点点就好。"),
        ("唐小满线 05：倒计时贴纸", "一百天计划", "图书馆", "tang", "倒计时墙",
         "唐小满在词汇书内页贴了一排倒计时贴纸，每完成一天就撕下一张。",
         "唐小满", "学长，你看。等最后一张撕掉，我们就会比现在厉害很多。",
         "你", "如果中间有一天状态不好呢？",
         "唐小满", "那就一起慢一点。可是不许一个人偷偷放弃。"),
        ("唐小满线 06：低分之后", "失落的消息", "夜晚宿舍窗边", "tang", "陪她重新开始",
         "模拟考成绩出来后，唐小满一整天没有发打卡消息。晚上，她终于发来一句：学长，我是不是太笨了。",
         "唐小满", "明明已经很努力了，分数还是不好看。我今天有点不想装作元气满满。",
         "你", "那就不用装。今晚我陪你从最简单的词开始。",
         "唐小满", "……谢谢学长。明天我会重新打起精神，但今晚让我依赖你一下。"),
        ("唐小满线 07：换我陪你", "反过来的监督", "考场", "tang", "递来的热饮",
         "你的模拟考也失利了。走出教室时，唐小满没有像往常一样闹你，只把热饮递到你手里。",
         "唐小满", "学长，这次换我说：一次分数不代表什么。你教过我的。",
         "你", "学妹长大了。",
         "唐小满", "所以学长偶尔也可以依赖我。只许偶尔哦，不然我会太得意。"),
        ("唐小满线 08：最后一页", "写满批注的礼物", "结局场景", "tang", "错词本最后一页",
         "考试结束后，唐小满把那本厚厚的错词本塞给你。最后一页不是单词，而是一行认真写下的话。",
         "唐小满", "学长，这次换我来陪你复习。以后遇到难的事，也一起。",
         "你", "这是新的打卡约定？",
         "唐小满", "嗯。长期有效。学长不许反悔。"),

        ("公共主线 01：第一次模拟考试", "三人的复盘会", "考场", "su", "第一次模拟考",
         "第一次模拟考结束，三份成绩单摊在活动室桌面。进步和失误都无处隐藏。",
         "苏晚晴", "学弟，今天不只看分数。我们把最容易丢分的词重新整理一遍。",
         "你", "这次我想把大家的错题都接住。",
         "苏晚晴", "好。那我也把自己的紧张交给你一点。"),
        ("公共主线 02：英语社经费危机", "一起守住活动室", "英语社活动室", "tang", "经费申请书",
         "活动室可能被收回的消息来得突然。桌上堆满申请材料，原本的复习计划被迫暂停。",
         "唐小满", "学长，这里不能消失。我们的打卡墙还没有贴满呢。",
         "你", "先把申请书需要的英文说明写好。",
         "唐小满", "嗯！我负责整理，学长负责陪我坚持到最后。"),
        ("公共主线 03：校级英语演讲", "所有人的舞台", "英语社活动室", "lin", "演讲彩排",
         "校级演讲成为保住活动室的关键。彩排结束后，林知夏合上计时器，表情比平时更认真。",
         "林知夏", "学弟，你的发音还有两处不稳。但比第一次见面时，已经像样很多。",
         "你", "这是林学姐版本的鼓励？",
         "林知夏", "别得寸进尺。正式上台前，我会再陪你练一遍。"),
        ("公共主线 04：一百天倒计时", "写下共同目标", "自习室", "su", "倒计时白板",
         "倒计时白板翻到一百天。活动室安静了一会儿，每个人都在那串数字前停下目光。",
         "苏晚晴", "学弟，一百天听起来很长，真正走起来却很快。别把自己逼得太紧。",
         "你", "那学姐也要答应我，累的时候说出来。",
         "苏晚晴", "好。我们互相监督，也互相照顾。"),
        ("公共主线 05：最后的路线选择", "最在意的人", "图书馆", "tang", "留给谁的位置",
         "图书馆只剩一个靠窗座位。你翻开词汇书时，发现里面夹着三张不同颜色的便签。",
         "唐小满", "学长，最近总觉得时间过得好快。考试结束以后，我们还会像现在这样见面吗？",
         "你", "有些约定不会因为考试结束就作废。",
         "唐小满", "那我先记住这句话。学长以后不许赖账。"),
        ("公共主线 06：考研前夜", "最后十个词", "夜晚宿舍窗边", "lin", "考研前夜",
         "考研前夜，群聊里没有人继续刷题。最后十个词安静地躺在你面前，像一路走来的坐标。",
         "林知夏", "学弟，今晚答完就休息。你已经做得足够多了。别让我隔着屏幕还要担心你。",
         "你", "明天之后，好像一切都会改变。",
         "林知夏", "会改变。但有些位置、一些约定，还有想见的人，不会。"),
    ]
    chapters = []
    public = [
        ("序章 01：掉在及格线外", "分班测试失败", "大学校门", "你盯着分班测试的红色分数，第一次认真承认：考研英语不会因为逃避而消失。"),
        ("序章 02：佳瑞英语社", "加入佳瑞英语社", "英语社活动室", "苏晚晴把报名表推到你面前。靠窗的桌面上，三本词汇书摊开，像三条尚未选择的路。"),
        ("序章 03：第一次并肩", "第一次单词挑战", "自习室", "林知夏抱着资料坐到对面，唐小满从门边探头。今晚，你要完成第一次真正的挑战。"),
    ]
    routes = [
        ("lin", "林知夏", ["错题本边缘", "无声的较量", "雨天留座", "阅读理解之夜", "模拟考前夕", "并肩的距离", "交换书签", "考场门口"]),
        ("su", "苏晚晴", ["靠窗的位置", "迎新演讲", "咖啡店改稿", "社长的疲惫", "夜晚窗边", "校级演讲", "坦率的停顿", "约定之后"]),
        ("tang", "唐小满", ["学妹的错词本", "操场打卡", "易混词警报", "一起补课", "倒计时贴纸", "低分之后", "换我陪你", "最后一页"]),
    ]
    commons = ["第一次模拟考试", "英语社经费危机", "校级英语演讲", "一百天倒计时", "最后的路线选择", "考研前夜"]
    continuations = {
        "lin": [
            ("旁白", "她低头翻过一页笔记，笔尖却在纸面上停了片刻。窗外的光落在她的侧脸上，让那份刻意维持的冷静显得没有平时那么牢固。", "normal"),
            ("林知夏", "还有，学弟。别只顾着猜我在想什么。把今天该记住的词答完，我会认真听你的答案。", "serious"),
            ("你", "只是单词的答案？", "normal"),
            ("林知夏", "……先从单词开始。其他的，等你再靠近一点自己确认。", "shy"),
        ],
        "su": [
            ("旁白", "她把便签推到你面前，自己却没有立刻收回手。短暂的安静里，原本普通的复习约定像是多了一层没有说破的含义。", "normal"),
            ("苏晚晴", "学弟，今天也别急着赶进度。认真陪我把这一段走完，好吗？", "smile"),
            ("你", "学姐这样问，我很难拒绝。", "normal"),
            ("苏晚晴", "那就别拒绝。偶尔让我任性一点，只把你的时间留在这里。", "shy"),
        ],
        "tang": [
            ("旁白", "她把错词本抱在胸前，明明刚才还很有气势，被你看久了却先移开视线。便签纸在风里轻轻晃动。", "normal"),
            ("唐小满", "学长，今天的约定还没有结束。答题的时候要认真看着我，不许偷偷走神。", "serious"),
            ("你", "如果是因为看着你才走神呢？", "normal"),
            ("唐小满", "那、那也要先答对。答对以后，我可以再让学长多看一会儿。", "shy"),
        ],
    }
    choice_styles = {
        "lin": [
            ["告诉她，你会认真追上她的步伐", "故意问她是不是只对你这么严格", "把她的提醒写在错题本最醒目的位置"],
            ["接过她递来的笔，靠近一点一起看笔记", "说你更在意她真实的想法", "安静陪她把没说完的话说完"],
            ["答应会记得今天，也记得她的偏心", "轻声问她考完以后是否还会留座", "坦率告诉她：你想继续留在她身边"],
        ],
        "su": [
            ["认真接住她的关心，也提醒她照顾自己", "笑着问这是不是学姐给你的特别待遇", "把她的便签仔细夹进词汇书"],
            ["告诉她，你愿意陪她把压力分担一点", "先不追问，只坐在她身边陪一会儿", "把自己的紧张也坦率交给她"],
            ["答应明天仍会来见她", "告诉她不必总在你面前逞强", "问她考试结束后是否还愿意保留这个位置"],
        ],
        "tang": [
            ["陪她把今天的打卡认真完成", "笑着提醒她，撒娇不能代替复习", "把自己的错词本也交给她检查"],
            ["答应和她一起把最难的部分拆开", "认真夸她已经比昨天进步", "伸手接住她递来的便签，约好明天继续"],
            ["告诉她，以后的打卡也不会缺席", "允许她偶尔依赖你，也请她监督你", "轻声答应：重要的约定不会过期"],
        ],
    }
    def make(cid, title, subtitle, scene, intro, char_id=None):
        title, subtitle, scene, char_id, anchor, opening, heroine, heroine_line, player, player_line, heroine2, heroine_line2 = beats[cid - 1]
        start = ((cid - 1) * 11) % len(words)
        points = [words[(start + i) % len(words)]["id"] for i in range(10)]
        dialogue = [
            {"speaker": "旁白", "text": opening, "expression": "normal"},
            {"speaker": heroine, "text": heroine_line, "expression": "serious"},
            {"speaker": player, "text": player_line, "expression": "normal"},
            {"speaker": heroine2, "text": heroine_line2, "expression": "shy"},
        ]
        dialogue.extend({"speaker": speaker, "text": text, "expression": expression} for speaker, text, expression in continuations[char_id])
        styles = choice_styles[char_id]
        choice_rounds = [
            [{"text": f"{styles[0][0]}：关于{anchor}", "effect": {"affection": 3, "trust": 2, "resonance": 1}},
             {"text": styles[0][1], "effect": {"affection": 2, "trust": 1, "resonance": 2}},
             {"text": styles[0][2], "effect": {"affection": 1, "trust": 3, "resonance": 1}}],
            [{"text": styles[1][0], "effect": {"affection": 3, "trust": 2, "resonance": 2}},
             {"text": styles[1][1], "effect": {"affection": 2, "trust": 3, "resonance": 2}},
             {"text": styles[1][2], "effect": {"affection": 2, "trust": 2, "resonance": 3}}],
            [{"text": styles[2][0], "effect": {"affection": 3, "trust": 2, "resonance": 3}},
             {"text": styles[2][1], "effect": {"affection": 3, "trust": 3, "resonance": 2}},
             {"text": styles[2][2], "effect": {"affection": 2, "trust": 2, "resonance": 3}}],
        ]
        return {"id": cid, "title": title, "subtitle": subtitle, "scene": scene, "character": char_id, "dialogue": dialogue, "word_ids": points,
                "choices": choice_rounds[0], "choice_rounds": choice_rounds,
                "unlock_score": 60}
    cid = 1
    for title, subtitle, scene, intro in public:
        chapters.append(make(cid, title, subtitle, scene, intro, ["su", "su", "lin"][cid-1])); cid += 1
    for route_id, name, names in routes:
        for no, title in enumerate(names, 1):
            scenes = ["图书馆", "自习室", "雨天校道", "咖啡店", "操场黄昏", "夜晚宿舍窗边", "考场", "结局场景"]
            chapters.append(make(cid, f"{name}线 {no:02d}：{title}", f"{name}的故事", scenes[no-1], f"你和{name}的约定又向前走了一步。那些反复出现的单词，也渐渐有了只属于这段时间的温度。", route_id)); cid += 1
    for no, title in enumerate(commons, 1):
        chapters.append(make(cid, f"公共主线 {no:02d}：{title}", "考研倒计时", ["考场", "英语社活动室", "英语社活动室", "自习室", "图书馆", "考场"][no-1], f"英语社所有人的进度汇在一起。{title}让你意识到，上岸从来不是一个人的独角戏。", ["lin", "su", "tang"][no % 3])); cid += 1
    return chapters

words = load_words()
avalanche_words = load_avalanche_words()
chapters = build_chapters(words)
endings = [{"character": c["id"], "name": c["name"], "normal": "只是朋友：你们在佳瑞英语社的合照里并肩微笑。", "good": "确认心意：她在结局场景里回应了你的认真。", "true": c["ending"]} for c in characters]
data = {"characters": characters, "words": words, "chapters": chapters, "endings": endings, "special_events": special_events}

(ROOT / "data").mkdir(exist_ok=True)
for name, value in [("characters", characters), ("words", words), ("chapters", chapters), ("choices", [{"chapter": c["id"], "choices": c["choices"]} for c in chapters]), ("endings", endings), ("special-events", special_events)]:
    (ROOT / "data" / f"{name}.json").write_text(json.dumps(value, ensure_ascii=False, indent=2), encoding="utf-8")
(ROOT / "data" / "generated-data.js").write_text("window.GAME_DATA = " + json.dumps(data, ensure_ascii=False) + ";\n", encoding="utf-8")
(ROOT / "data" / "avalanche-words.json").write_text(json.dumps(avalanche_words, ensure_ascii=False, indent=2), encoding="utf-8")
(ROOT / "data" / "avalanche-words.js").write_text("window.AVALANCHE_WORDS = " + json.dumps(avalanche_words, ensure_ascii=False) + ";\n", encoding="utf-8")
print(f"generated {len(words)} words, {len(avalanche_words)} avalanche words and {len(chapters)} chapters")
