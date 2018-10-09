// 导航栏高度
var navHeight = $('nav').height()
console.log(navHeight)
// 为body加一个导航栏高度的透明div,给导航栏一个位置
$('.content-body').css('margin-top',navHeight*2)
