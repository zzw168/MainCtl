    

    let  timeVal =null
    let now = 0

    // 创建一个新的Audio对象
var audio = document.getElementById("myAudio");
// 播放音频
let playHTL = document.getElementById('playButton').innerHTML
    function playAudio() {
    audio.addEventListener('playing', function(e) {
        console.log('playing',e);
        document.getElementById('playButton').innerHTML = "pause"
    }); 
    audio.addEventListener('ended', function() {
        console.log('音频播放结束');
        document.getElementById('playButton').innerHTML = 'play'
    });
    audio.play().catch(error => {
                if (error.name === "NotAllowedError") {
                    console.log("Auto-play was prevented, invoking user action may start playback");
                    // 引导用户进行交互，比如点击按钮来启动播放
                    //  document.getElementById('playButton').style.display = 'block';
                    // document.getElementById('muted').style.display = 'block';
                    document.getElementById('playButton').onclick = function() {
                        audio.play().catch(error => {
                            console.error("Playback failed:", error);
                        });
                    };
                }
            });
  }

  document.getElementById('playButton').addEventListener('click', function() {
    let playHTL = document.getElementById('playButton').innerHTML
    
    playAudio();
    
  });

window.onload = ()=>{
    document.getElementById('playButton').click();
    console.log(" document.getElementById('playButton').click();", document.getElementById('playButton'))
}

    const toRunTime =(days)=>{
    clearInterval(timeVal)
    // 定位时钟模块
    $("#clock").show()
    $(".weihu").hide()
    $(".txt2").show()
    let clock = document.getElementById('clock')
    now = days
    if(clock){

    let flips =clock?.querySelectorAll('.flip')
    console.log("flips",flips)
    $('#clock').html('Next Race <span class="padLeft">  #'+ days+"  </span>")
    // let cutNow = now
    
    }}
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
    $("#clock").show()
    $('#clock').html('<span>赛道维护</span>')

}

// // 测试
if(config.test){
  
    renderFn(datalist,()=>{
//        toRunTime(9555060)
//        weihuFn()
        setTimeout(()=>{
//           renderFn(datalist)
          toRunTime(9555060)
        },3000)
      })
}

getSocketFn({
    port:config.port
},(res,nTime)=>{
   
    if(res.type=='updata'){
       
    //    console.log("updata msg socket",res)
       renderFn(res.data)
    }else if(res.type=='time'){
       // 时间
       toRunTime(res.data )
    //    console.log("time msg socket",res)
    }
    else if(res.type=='stop'){
       // 时间
       weihuFn(res.data)
    //    console.log("stop msg socket",res)
    }
})
