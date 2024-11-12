    
	let config =  {
        url:"127.0.0.1",
        port:8888,
        rankUrl:"jiesuan",
        test:1
    }
    // 右边数据 赛道 长度
    var rtxt1='20.5m'
    var  rtxt2=10
    var  rtxt3=2

    let  timeVal =null
    let now = 0
    //  $.get(config.url+":"+config.port+config.rankUrl).then(
    //  res=>{
    //     // console.log("config",JSON.parse(res),typeof(res),res[0] )
    //     renderFn( JSON.parse(res))
    // }).fail((err)=>{
    //     console.log("err",err)
    //   }
    //  )
     //=========启动一个websocket
    //  $(_=>{ 
    //  })

     const toRunTime =(days)=>{
        clearInterval(timeVal)
  // 定位时钟模块
  $("#clock").show()
  $(".weihu").hide()
  $(".txt2").show()
  let clock = document.getElementById('clock')
  // 定位6个翻板
  let flipObjs = []
  now = days
  if(clock){


  let flips =clock?.querySelectorAll('.flip')
  console.log("flips",flips)
  // 获取当前时间

  // 格式化当前时间，例如现在是20:30:10，则输出"203010"字符串
  let nowTimeStr = formatSeconds(new Date(now), 'hhiiss')
  // 格式化下一秒的时间
  let nextTimeStr = formatSeconds(new Date(now + 1), 'hhiiss')
  // 定义牌板数组，用来存储6个Flipper翻板对象
  console.log("nextTimeStr",now + 1,nextTimeStr,flips)
  
  for (let i = 0; i < flips.length; i++) {

  }
  }
  // let cutNow = now
  timeVal = setInterval(function() {
    
      // 获取当前时间
      console.log("flipObjs",now)
      // 格式化当前时间
      let nowTimeStr = formatSeconds(new Date(now), 'hhiiss')
      // 格式化下一秒时间
      let nextTimeStr = formatSeconds(new Date(now-1), 'hhiiss')
      // 将当前时间和下一秒时间逐位对比
      for (let i = 0; i < flipObjs?.length; i++) {
          // 如果前后数字没有变化，则直接跳过，不翻牌
          if (nowTimeStr[i] === nextTimeStr[i]) {
              continue
          }
          // 传递前后牌的数字，进行向下翻牌动画
          flipObjs[i].flipDown('number' + nowTimeStr[i], 'number' + nextTimeStr[i])
 
      }
   
      now -= 1
      if(now<0){
        now=0
      }
      $('#clock').html('Next Game：'+(now)+' s')
      if(now==0){
        clearInterval(timeVal)
      }
  }, 1000)

}
function formatSeconds(seconds) {
    const hours = Math.floor(seconds / 3600);
    const minutes = Math.floor((seconds % 3600) / 60);
    const secs = seconds % 60;

    const formattedHours = String(hours).padStart(2, '0');
    const formattedMinutes = String(minutes).padStart(2, '0');
    const formattedSeconds = String(secs).padStart(2, '0');

    return `${formattedHours}${formattedMinutes}${formattedSeconds}`;
}


const weihuFn=(text)=>{
    clearInterval(timeVal)
    $("#clock").hide()
    $(".txt2").hide()
//   $("#coutDown .weihu").show().html(`${text||'赛道维护'}</div>`)
  $("#clock").html('赛道维护')
}

// // 测试



var Socket1;
Socket1 = $.websocket({
     domain:config.url,   //这是与服务器的域名或IP
     port:config.port,                  //这是服务器端口号
     protocol:config.rankUrl,            //这东西可有可无,组合起来就是 ws://www.qhnovel.com:8080/test
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
     let res = JSON.parse(result)
         if(result == 'pong'){
             console.log('pong');
             //如果获取到消息，心跳检测重置 
             //拿到任何消息都说明当前连接是正常的 
             heartCheck.reset().start();
         }
         if(res.type=='updata'){
            
            console.log("updata msg socket",res)
            renderFn(res.data)
         }else if(res.type=='time'){
            // 时间
            toRunTime(res.data )
            console.log("time msg socket",res)
         }
         else if(res.type=='stop'){
            // 时间
            weihuFn(res.data)
            console.log("stop msg socket",res)
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
             console.log('未收到pong，后端已断开');
             Socket1.close(); 
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