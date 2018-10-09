// 首页封面 背景图最大显示
var wh = window.innerHeight;
$('.content-header').css({'height':wh+'px'});

// 首页封面 向下按钮弹跳
$('#content-header-circle a').hover(
    function () { 
        $('#content-header-circle img').attr('class',"animated infinite bounce")
},
    function(){
        $('#content-header-circle img').attr('class',"")
}
)


// 导航栏高度
var navHeight = $('nav').height()

//首页导航 自动变色
// $(this).scroll(function(){
//     if (scrollY >= (wh + navHeight)){
//         $('nav').removeClass('navbar-inverse')
//     }else{
//         $('nav').addClass('navbar-inverse')
//     }
// })

// 为body加一个导航栏高度的透明div,给导航栏一个位置
$('.blank').height(navHeight)

