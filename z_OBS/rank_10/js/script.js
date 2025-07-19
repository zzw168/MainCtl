var spacing = 0
var offset = 62;
var count = 0;
var positions = [];
var scoketUrl = "127.0.0.1"  //这是与服务器的域名或IP
var port = 9999
var isTest = 0
var spech = 400 //速度 默认速度
let thres = 10  //阈值 
var spechs = null //记录上一次sokcet 消息过来的时间戳
let testData = [3, 2, 4, 1, 5, 6,7,8,9,10]
let rankSuiOld =[]
let pstNumArr=  [{idx:1,name:'A',time:'20:39'},
                {idx:2,name:'B',time:'20:39'},
                {idx:3,name:'C',time:'20:39'},
                {idx:4,name:'D',time:'20:39'},
                {idx:5,name:'E',time:'20:39'},
                {idx:6,name:'F',time:'20:39'},
                {idx:7,name:'F',time:'20:39'},
                {idx:8,name:'F',time:'20:39'},
                {idx:9,name:'F',time:'20:39'},
                {idx:10,name:'F',time:'20:39'}
                ]
            $(_=>{
               pstNumArr.forEach(function(el,i) {
                let htm = `<li data-origin="0px" class="list-item" style="float: none;left: 0px;">
                <div class="rank_idx flex-box center " style="color:#333;background:rgba(247,247,247,.5);height:62px;width:50px" >  <p><font size="6">${i+1} </font></p> </div> 
                <div class="rank_label ranks${el.idx-1} flex-box center">
       
                <img src="./img/${el.idx}.png" />
          
                </div> 
                <div class="time rank_label flex-box center"><div class="flex-box tBox center" style="display:none;">${el.time}</div> </div>
             </li>`
            //     
                $("ul.letters").append(htm)
               
            })
        
              
           
            //        <div class="time rank_label flex-box"><div>${el.time}</div> </div> 
           $(".list-item").each(function(e) {
        
                the_position = spacing ;
                positions.push(the_position);
                $(this).css("top", the_position);
                $(this).find(".rank_idx").eq(0).css('background', `url(./img/${e+1}.png) no-repeat 100% 100%)`);
                $(this).attr("data-origin", the_position);
                $(this).attr("data-idx", e);
                spacing += offset;
                count++
               
            });

            })

            $(_=>{
              window.computeWin =  setInterval(() => {
                    let ballWin = $("ul.letters .rank_label img").eq(0).outerWidth(true)
                    if (ballWin>0) {
                        
                   clearInterval( window.computeWin)
                    $(".list-item").each(function(e) {
                       
                        $(this).find('.time').css("left",80+ballWin+'px')
                        console.log("rank_label",ballWin)
                        })
                    }
                }, 1);
              
            })
            function getStyle(obj,style){
                return obj.currentStyle?obj.currentStyle[style]:getComputedStyle(obj,false)[style];
            }
            //原生js动画类似jquery--animate
            function animate(obj,styleJson,callback){
                console.log("(testData.length+1)",(testData.length+1))
                clearInterval(obj.timer);
                // 开启定时器
                obj.timer=setInterval(function(){
                    var flag=true;//假设所有动作都已完成成立。
                    for(var styleName in styleJson){
                        //1.取当前属性值
                        var iMov=0;
                        // 透明度是小数，所以得单独处理
                        iMov=styleName=='opacity'?Math.round(parseFloat(getStyle(obj,styleName))*100):parseInt(getStyle(obj,styleName));
        
                        //2.计算速度
                        var speed=0;
                        speed=(styleJson[styleName]-iMov)/(testData.length);//缓冲处理，这边也可以是固定值
                        speed=speed>0?Math.ceil(speed):Math.floor(speed);//区分透明度及小数点，向上取整，向下取整
                        
                        //3.判断是否到达预定值
                        if(styleJson[styleName]!=iMov){
                            flag=false;
                            if(styleName=='opacity'){//判断结果是否为透明度
                                obj.style[styleName]=(iMov+speed)/100;
                                obj.style.filter='alpha(opacity:'+(iMov+speed)+')';
                            }else{
                              obj.style[styleName]=iMov+speed+'px';
                            }
                        }
                    }
                    if(flag){//到达设定值，停止定时器，执行回调
                        clearInterval(obj.timer);
                        if(callback){callback();}
                    }
                },60)
            }
            var y = [];
// $("ul.letters li").css("float", "none").css("position", "absolute");
// socArr {"mc":1,data:时间戳}
function toRunSortRank(socArr,isTime){
    window.isRest = false
    
    $(this).addClass('aniFont')
    var u = positions.slice(0);
    // console.log("background: #333;as",c)
    let ballWin = $("ul.letters .rank_label img").eq(0).outerWidth(true)
    
    y =fisherYates(u);
    // socketRank()
    // $("ul.letters li").each(function(i) {
       
    // })
    $('[class*=ranks]').stop()
    let ct = (new Date().getTime() - spechs )

    $("ul.letters li").each(function(i) {

        let spechss =  spechs&&(ct<spech)?(ct+(thres+i)):spech
        
        let rNo = $(this).attr('data-origin')
        $(this).find('.rank_label').removeClass('aniFont')
        let inds =  $(this).index()
      
   
        console.log("sssdfff222",isTime,inds+1,socArr[i],ct,spechss,positions[i] / offset)
      
        if(socArr[i]){
            console.log("sssdfff222",ct,spechss,positions[i] / offset)
            $('.ranks'+(socArr[i]-1)).animate({
                top: ((positions[i])) +'px',
            },spechss,()=>{
             
                //  $('.ranks'+(socArr[i]-1)).stop()
            })
            //  $('.ranks'+(socArr[i]-1)).stop()
        }
        let timeDom = $(this).find('.rank_label').eq(1)

        console.log("dsdsd",ct,spechss,positions[i] / offset)
        if( isTime&&inds+1==socArr.mc||isTest){
            //  $('.ranks'+(socArr[i]-1)).stop()

           timeDom.hide()
            if(['TRAP','OUT'].includes(socArr.data)||isTest){
                timeDom.css({
                    background:"#e8a73f"
                })
                if(isTest) socArr.data = 'OUT'
                let imgsrc='fly'
                if(socArr.data=='TRAP'){
                  
                    imgsrc='ka'
                }
            let qiuHtml =`<img class="kaImg" src="./img/${imgsrc}.png"    style="" />
            <span class="kaTxt" style="margin-left:2px">${socArr.data}</span>` 



            timeDom.addClass('aniFont').find('div').addClass('kaBox').removeClass('center').html(qiuHtml)
            }else{



                timeDom.addClass('aniFont').find('div').addClass('center').html(socArr.data)
            }
    
            //  window.desyTime =  setTimeout(_=>{
               timeDom.show()
               timeDom.find('div').show()
                // clearTimeout( window.desyTime)
        
               
            window.isRest = false
            return
     
            y.splice(0, 1) 
    }
    spechs = new Date().getTime()
    rankSuiOld = socArr
    
    })
   

    
}


function socketRank(c,posArr) {
    var a = c.length;
    let arrs =[]
    if (a == 0) {
        return false
    }
    // console.log("arrs",posArr,c)
    for(var i=0;i<=a-1 ; i++){
     console.log("arrs",posArr,c)
        arrs[i] = posArr[c[i]-1] 
    }
    // 随机数
    
    return arrs
}


function parseTime(time, cFormat) {
    if (arguments.length === 0) {
      return null
    }
    const format = cFormat || '{y}-{m}-{d} {h}:{i}:{s}'
    let date
    if (typeof time === 'object') {
      date = time
    } else {
      if ((typeof time === 'string') && (/^[0-9]+$/.test(time))) {
        time = parseInt(time)
      }
      if ((typeof time === 'number') && (time.toString().length === 10)) {
        time = time * 1000
      }
      date = new Date(time)
    }
    const formatObj = {
      y: date.getFullYear(),
      m: date.getMonth() + 1,
      d: date.getDate(),
      h: date.getHours(),
      i: date.getMinutes(),
      s: date.getSeconds(),
      a: date.getDay()
    }
    let time_str = format.replace(/{(y|m|d|h|i|s|a)+}/g, (result, key) => {
      let value = formatObj[key]
      // Note: getDay() returns 0 on Sunday
      if (key === 'a') {
        return ['日', '一', '二', '三', '四', '五', '六'][value]
      }
      if (result.length > 0 && value < 10) {
        value = '0' + value
      }
      return value || 0
    })
    time_str = time_str==='0-0-0 0:0:0'?'':time_str
    return time_str
  }

function  getSuiJi(min = 0, max = 10) {
    min = Math.ceil(min)
    max = Math.ceil(max)
    return Math.floor(Math.random() * (max - min) + min)
}
function fisherYates(array,t) {
    var a = array.length;
    if (a == 0) {
        return false
    }
    if(t) {
        var sui = getSuiJi(1,a+1)
        console.log("sui",sui)
        return { data:parseTime(new Date,'{h}:{i}:{s}'),
               mc:sui
           }
    }
    for (let i = array.length - 1; i > 0; i--) {
        let j = Math.floor(Math.random() * (i + 1));
        [array[i], array[j]] = [array[j], array[i]];
      }
  return array;
}

function startRun(testArr){
    //  window.timerV = setInterval(_=>{
         
        let rankSui =  fisherYates(testArr)
        // spechs = new Date().getTime()
        toRunSortRank(rankSui,1)
        // window.outime = setTimeout(_=>{
        //     let suiji =  fisherYates(testArr,1)
        //     console.log('suiji',suiji)
        //      toRunSortRank(suiji,1)
        //      clearTimeout( window.outime )
        //  },500*2)
    //  },spech)
}
function resetFn(){
    window.isRest = 1
    if(window.timerV) clearInterval( window.timerV)
    if(window.outime) clearTimeout( window.outime )
    if(window.desyTime) clearTimeout( window.desyTime )

    $("ul.letters li").each(function(e,i) {
     
        let rNo = $(this).attr('data-origin')
        console.log("sdsd",rNo,e, positions[e])
        $('.ranks'+e).stop()
        // $(this).find('.rank_label.time >div').stop()
        $(".ranks"+e).animate({
            top: (positions[e])+'px'
        })
        $(this).find('.rank_label.time').removeClass('aniFont')
        $(this).find('.rank_label.time').hide()
        $(this).find('.rank_label.time >div').text('00:00').hide()
    })
   

}
if(isTest){
    $(_=>{
        $("#restore").show()
        $("#shuffle").show()
        $("#stop").show()
        
    })
    
    startRun(testData)
        setTimeout(_=>{
                   let suiji =  fisherYates(positions,1)
                   console.log('suiji',suiji)
                    toRunSortRank(suiji,1)
                },1000*3)
}

$("#shuffle").on('click',function(){
   
    startRun(testData)
})
$("#stop").on('click',function(){
   
    $("ul.letters li").each(function(e,i) {
        $('.ranks'+e).stop()
        // $(this).find('.rank_label.time >div').stop()



    })
   
   if(window.timerV) clearInterval( window.timerV)
})

$("#restore").on('click',function(){
    resetFn()
});
//=========启动一个websocket
var Socket1;
Socket1 = $.websocket({
    domain:scoketUrl||"192.168.1.25",   //这是与服务器的域名或IP
     port:port||9999,                  //这是服务器端口号
     protocol:"",            //这东西可有可无,组合起来就是 ws://www.qhnovel.com:8080/test
     onOpen:function(event){
        //  alert("已经与服务端握手,onOpen可省略不写");
         heartCheck.reset().start(); //传递心跳信息
     },
     onError:function(event){
        //  alert("发生了错误,onError可省略不写");
        console.log("  reconnect();",event)
         reconnect();//断开重连
     },
     onSend:function(msg){
        //  alert("发送数据额外的代码,可省略不写");
          if(sen_flag == 2){
             //已经ping过去了
             console.log('ping');
         } else{
            console.log('msgmsg',msg);
          
             //用来处理正常的聊天室消息
         }
     },
     onClose:function(e){
        console.log("close",e)
        reconnect();//断开重连
     },
     onMessage:function(result,nTime){
     //我这用result == 'pong'有个大大大的前提，就是ping给后台的时候，后台是直接推送pong回来给我的，所以我这里可以直接的判断result == 'pong'
    
         if(result == 'pong'){
             //如果获取到消息，心跳检测重置 
             //拿到任何消息都说明当前连接是正常的 
             heartCheck.reset().start();
         }else{
            let res = JSON.parse(result)
            if(res.type=='pm'){
                toRunSortRank(res.data)
             }else if(res.type=='time'){
                // 时间
                toRunSortRank( res,1)
             }
             else if(res.type=='zc'){
                // 时间
                resetFn()
             }
         }
      
        //  alert("从服务端收到的数据:" + result);
        //  alert("最近一次发送数据到现在接收一共使用时间:" + nTime);
     }
 });
//这个是我在具体项目中用来辨别心跳和正常消息的标志位
var sen_flag = 1;
//避免重复连接 
var lockReconnect = false;
// 重连函数
function reconnect(){
 console.log("websocket正在重新连接")
 if (lockReconnect) return; 
 lockReconnect = true; //没连接上会一直重连，设置延迟避免请求过多 
 setTimeout(function() { 
    Socket1.onInit();
     lockReconnect = false; 
 }, 5000);
}

//心跳检测
var heartCheck = {
 timeout: 60000, //60秒
 timeoutObj: null,
 serverTimeoutObj: null,
 reset: function() {
     clearTimeout(this.timeoutObj);
     clearTimeout(this.serverTimeoutObj);
     return this;
 },
 start: function() {
     var self = this;
     this.timeoutObj = setTimeout(function() {
         //这里发送一个心跳，后端收到后，返回一个心跳消息，
         //onmessage拿到返回的心跳就说明连接正常
         sen_flag = 2;
         Socket1.send("ping");
         sen_flag = 1;
         self.serverTimeoutObj = setTimeout(function() { //如果超过一定时间还没重置，说明后端主动断开了
             //console.log('未收到pong，后端已断开');
             //Socket1.close(); 
             //如果onclose会执行reconnect我们执行ws.close()就行了.如果直接执行reconnect 会触发onclose导致重连两次
         }, self.timeout)
     }, this.timeout)
 }
}
//当visibilityState流浪器的状态改变时，进行监听
document.addEventListener('visibilitychange',function() {
 if(document.visibilityState=='hidden') {
 //页面被隐藏或调到后台
                 
 }else{
 //页面还在时异常被关闭才进行重连
     console.log("Close回调函数，自动重连")
     reconnect();
 }
})