
var scoketUrl = "192.168.0.63"  //这是与服务器的域名或IP

const getIpFn = (cal)=>{
  cal(false)
    // $.ajax({
    //   url:"/ip",
    //   complete:(res)=>{
    //       // console.log("getSocketFn",res)
    //     cal(res?.responseText.indexOf('230')>-1?false:res?.responseText)
    //   }
    // })
    
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

const QueryParams =(k)=>{
  let url = window.location.search
  let  data = {},  ks
  console.log(" QueryParams ks",url)
  if(url.indexOf("?")>-1){
			
    let us = url.split("?")[1]
    url = url.split("?")[0]
    let usparams = us.split('&')
    usparams.forEach(element => {
      let sps =  element.split('=')
       ks = sps[0],vs = sps[1]
      data[ks] = vs
    });
    if(k) return data[k]
    return  data
  }
  
}
// 获取url参数

const QueryParams1 = (keys)=>{
  $(function () {
  let query =  new URLSearchParams()
  console.log("})",query,window.location)
  return query.get(keys)||{}
})
}

//=========封装 启动一个websocket
var Socket1;
function getSocketFn ({
    scoketUrl,   //这是与服务器的域名或IP
    port,
},onMessageCal){
    getIpFn(res=>{
       
    
        scoketUrl = scoketUrl||res||_config.ip
        console.log("scoketUrl",scoketUrl,res)
            Socket1 = $.websocket({
                 domain:scoketUrl||"127.0.0.1",   //这是与服务器的域名或IP
                 port:port||9999,                  //这是服务器端口号
                 protocol:"",            //这东西可有可无,组合起来就是 ws://www.qhnovel.com:8080/test
                 onOpen:function(event){
                    //  alert("已经与服务端握手,onOpen可省略不写");
                     lockReconnect = true; 
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
                 let res 
                 try {
                  res = JSON.parse(result)
                 } catch (error) {
                  res = result
                 }
                   
                     if(result == 'pong'){
                         console.log('pong');
                         //如果获取到消息，心跳检测重置 
                         //拿到任何消息都说明当前连接是正常的 
                         heartCheck.reset().start();
                     }
    
                     onMessageCal(res,nTime)
                    
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
            console.log("websocket正在重新连接",lockReconnect)
            if (lockReconnect) return; 
            lockReconnect = true; //没连接上会一直重连，设置延迟避免请求过多 
            setTimeout(function() { 
              lockReconnect = false; 
                Socket1.onInit();
                // 
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
    })
}



