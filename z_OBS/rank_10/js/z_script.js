//let pstNumArr = [{ idx: 1, position: 0 },
//{ idx: 2, position: 60  },
//{ idx: 3, position: 120  },
//{ idx: 4, position: 180  },
//{ idx: 5, position: 240  },
//{ idx: 6, position: 300  }
//];
var spacing = 0
var offset = 62;
var count = 0;
var scoketUrl = "127.0.0.1"  //这是与服务器的域名或IP
var port = 2222
var isTest = 0
var spech = 400 //速度 默认速度
let thres = 10  //阈值
var spechs = null //记录上一次sokcet 消息过来的时间戳

let testData = [3, 2, 4, 1, 5, 6,7,8,9,10]
let rankSuiOld =[]

let pstNumArr = []
var ballNum = 10 //球的数量
for(let i = 0; i<ballNum; i++){
    pstNumArr.push({idx:i+1,position:i*60,time:'20:39'});
}

$(_ => {
    pstNumArr.forEach((el, i) => {
        let htm = `<li data-origin="0px" class="list-item" style="float: none;left: 0px;">
                    <div class="rank_idx " ><img src="./img/l${el['idx']}.png" /> </div>
                    <div class="rank_label ranks${el['idx']} flex-box center">
                        <img src="./img/${el['idx']}.png" />
                    </div>
                    <div class="time rank_label flex-box center"><div class="flex-box tBox center" style="display:none;">${el.time}</div> </div>
                    </li>`
        $("ul.letters").append(htm)
    });
});

function getStyle(obj, style) {
    return obj.currentStyle ? obj.currentStyle[style] : getComputedStyle(obj, false)[style];
};
//原生js动画类似jquery--animate
function animate(obj, styleJson, callback) {
    clearInterval(obj.timer);
    // 开启定时器
    obj.timer = setInterval(function () {
        var flag = true;//假设所有动作都已完成成立。
        for (var styleName in styleJson) {
            //1.取当前属性值
            var iMov = 0;
            // 透明度是小数，所以得单独处理
            iMov = styleName == 'opacity' ? Math.round(parseFloat(getStyle(obj, styleName)) * 100) : parseInt(getStyle(obj, styleName));

            //2.计算速度
            var speed = 0;
            speed = (styleJson[styleName] - iMov) / 8;//缓冲处理，这边也可以是固定值
            speed = speed > 0 ? Math.ceil(speed) : Math.floor(speed);//区分透明度及小数点，向上取整，向下取整

            //3.判断是否到达预定值
            if (styleJson[styleName] != iMov) {
                flag = false;
                if (styleName == 'opacity') {//判断结果是否为透明度
                    obj.style[styleName] = (iMov + speed) / 100;
                    obj.style.filter = 'alpha(opacity:' + (iMov + speed) + ')';
                } else {
                    obj.style[styleName] = iMov + speed + 'px';
                }
            }
        }
        if (flag) {//到达设定值，停止定时器，执行回调
            clearInterval(obj.timer);
            if (callback) { callback(); }
        }
    }, 60)
};

function toRunSortRank(socArr){
    if (socArr){
        console.log("socArr :",socArr)
        socArr.forEach((el, i) =>{
//            console.log("socArr :",socArr[i])
            $('.ranks' + (socArr[i])).stop()    // 停止动画
            $('.ranks' + (socArr[i])).animate({ //移动动画
                top: (pstNumArr[i]["position"]) + 'px',
            });
        })
    }
};

//=========启动一个websocket
var Socket1;
Socket1 = $.websocket({
    domain: scoketUrl||"127.0.0.1",   //这是与服务器的域名或IP
    port: port||2222,                  //这是服务器端口号
    protocol: "",            //这东西可有可无,组合起来就是 ws://www.qhnovel.com:8080/test
    onOpen: function (event) {
        //  alert("已经与服务端握手,onOpen可省略不写");
        heartCheck.reset().start(); //传递心跳信息
    },
    onError: function (event) {
        //  alert("发生了错误,onError可省略不写");
        console.log("reconnect();", event)
        reconnect();//断开重连
    },
    onSend: function (msg) {
        //  alert("发送数据额外的代码,可省略不写");
        console.log('ping:', msg);
        //用来处理正常的聊天室消息
    },
    onClose: function (e) {
        console.log("close", e)
        reconnect();//断开重连
    },
    onMessage: function (result, nTime) {
        // console.log(result);
        if(result == 'pong'){
            //如果获取到消息，心跳检测重置
            //拿到任何消息都说明当前连接是正常的
            heartCheck.reset().start();
        }else{
            let res = JSON.parse(result)
            if (res.type == 'pm') {
                console.log("pm msg socket:", res)
                toRunSortRank(res.data)
            } else if(res.type=='time'){
                // 时间
                toRunSortRank( res,1)
            } else if(res.type=='zc'){
                // 时间
                resetFn()
            } else {
                console.log("msg socket:", res)
            }
        }
    }
});
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
// 重连函数
function reconnect() {
    console.log("websocket正在重新连接")
    setTimeout(_=>{
        location.reload();
    }, 5000)
}
//当visibilityState流浪器的状态改变时，进行监听
document.addEventListener('visibilitychange', function () {
    if (document.visibilityState == 'hidden') {
        //页面被隐藏或调到后台

    } else {
        //页面还在时异常被关闭才进行重连
//        console.log("Close回调函数，自动重连")
//        reconnect();
    })
})


