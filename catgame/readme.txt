1、让chatgpt用math.random()写了一个剪刀石头布游戏（见catgamebygpt.html）。
2、在游戏流程上缺乏“导语”、“下一轮”等提示，且没有给出“对方”的选择，只有“你输了””平局“的结果，体验较差。
3、增添了”你的选择“提示语。
4、用 nextRoundBtn.addEventListener函数将之前的变量清空，添加”下一轮“按钮，实现了重复进行功能
5、为了增强交互体验设计了虚拟交互对象”小猫“，添加小猫gif图片增加生动性，同时为每一个结果添加相应的小猫图片”你赢了“——catsad.jpg；”你输了“——cathappy.jpg，用const catImage = document.querySelector('.introduction_image')和catImage.src实现图片的转换。
6、更改按钮颜色，hover颜色，字体大小，间距等，美化界面。
