# 美术资源说明

首版角色立绘由项目用户提供并明确要求直接用于原型。版权来源尚未核验，因此仅限本地原型演示，不应直接用于公开发布、商业发行或素材再分发。

- 角色立绘：`assets/characters/` 中保留三张用户提供的 JPEG 参考图，并新增 18 张画师感上半身 PNG 差分。游戏按剧情状态切换普通、微笑、害羞、认真、吃醋、失落六种图片。
- 隐藏彩蛋角色：`assets/characters/banana-kun.jpg` 为用户提供的参考图，仅用于原型演示。公开发布前应确认其拥有使用和传播权限；如不确定，请替换为原创绘制版本。
- 彩蛋角色：`assets/characters/zhang-avalanche.jpg` 为用户提供的张雪崩老师参考图，仅用于原型演示。公开发布前应确认其拥有使用和传播权限；如不确定，请替换为原创绘制版本。
- 彩蛋角色：`assets/characters/jie-ge.jpg` 为用户提供的杰哥参考图，仅用于原型演示。公开发布前应确认其拥有使用和传播权限；如不确定，请替换为原创绘制版本。
- 背景：`assets/backgrounds/` 中包含 10 张原创 AI 生成校园场景 PNG 原稿及压缩 JPEG 运行版本。网页加载 JPEG，并保留 CSS 渐变作为加载失败时的回退。
- UI：项目内原创 CSS。
- BGM：`assets/audio/heavenly-loop.ogg` 与 `assets/audio/calm-loop.mp3`，来自 OpenGameArt，CC0。MP3 用作 Safari 和部分手机浏览器回退。

后续替换方式：

1. 对外发布前，在 `assets/characters/` 中放置原创或许可清晰的透明背景 WebP/PNG 立绘。
2. 在 `assets/backgrounds/` 中放置原创或许可清晰的 WebP/JPEG 背景。
3. 记录作者、原始链接、许可证和修改说明。
4. 优先使用原创委托、团队自制或 CC0 素材；不要使用已有动漫角色。

表情差分采用以下格式，网页会自动优先加载 PNG 差分，不存在时回退到普通状态：

- `lin-zhixia-normal.png`、`lin-zhixia-smile.png`、`lin-zhixia-shy.png`、`lin-zhixia-serious.png`、`lin-zhixia-jealous.png`、`lin-zhixia-sad.png`
- `su-wanqing-*.png`
- `tang-xiaoman-*.png`

具体绘图提示词见 `docs/美术提示词.md`。
