// 长度

const datalist ={
  qh:"9555059",
  rank:[
      
      {
        "mc": 10,
        "time": "138.18"
      },
      {
        "mc": 9,
        "time": "138.18"
      },
      {
        "mc": 8,
        "time": "138.18"
      },
      {
        "mc": 7,
        "time": "138.18"
      },
      {
        "mc": 6,
        "time": "138.18"
      },
      {
        "mc": 5,
        "time": "138.18"
      },
      {
        "mc": 4,
        "time": "138.18"
      },
      {
        "mc": 3,
        "time": "138.18"
      },
      {
        "mc": 2,
        "time": "138.18"
      },
      {
        "mc": 1,
        "time": "138.18"
      }
    
  ]
} 
// <div class="flex-box flex-end logo"><img style="display:none"  src="./img/logo.png" /></div> 
// 	  // <img  class="fonImg animate__animated animate__flipInX" src="./assets/fon.png" alt="" />
//            <div class="fonImg animate__animated animate__flipInX"></div> 
const FiltersStr = ['CHAMPION','SECOND PLACE','THIRD PLACE']
const renderFn = (data,cb)=>{
$("#wrap").html(`
<div class=" animate__animated animate__backInRight ">
      <div class="topView flex-box center">
    

        <div class="qh whiteA">Results Term <span class="padLeft ">${data.qh}</span></div>
        </div>
     </div>
     <div class="rankView flex-box between">
      <div class="rankItem "  >
          
          <div id="rank" class="flex-box column item-start between">
          </div>
        </div>
        <div class="view-right animate__animated animate__bounceInRight">
           
          <div class="pathBox flex-box center column animate__animated animate__backInRight">
           <div class="coutBox" >
            
                <div class="txt flex-box center ">${rTopTxt}</div>
            </div>  
            <img id="sphere" class="pathImg" src="./assets/pathBg.png" alt="" />
            <div class=" flex-box between wrap"> 
             <div class="rtxt fl  ">
                   <div> LENGTH</div>
                   <div class="rtxt1">
                            ${rtxt1}
                      </div>  
                </div> 
                <div class="rtxt fl ">
                    <div>TURN</div>
                        <div class="rtxt2">
                         ${rtxt2}
                      </div>  
                </div>  
            
                <div class="rtxt fl ">
                     <div>MARBLES</div>
                        <div class="rtxt3">
                         ${rtxt3}
                      </div>  
                </div>   
                  <div class="rtxt fl ">
                 <div>LAPS</div>
                  <div class="rtxt4">
                         ${rtxt4}
                      </div>  
                </div> 
               </div> 
          </div>
        </div>
      </div>
    </div>	
    <div id="coutDown" class="flex-box center animate__animated  animate__bounceInUp">
               <img id="next"  src="./assets/next.png" alt="" />
             <div class="clock"  id="clock">
            </div>
              <div class="weihu" style="display:none">${'赛道维护'}</div>
            </div>
`)
//    <img class=" fon2Img" src="./assets/fon2.png" alt="" />
$(_=>{
$('#rank').html('')
let htm = ''
  var rank = $('#rank') 
  // <img style="top:${(-(506/10)*i)+3}px" src="./assets/qiu.png" alt="" />
data.rank.forEach((el,i)=>{
{/* <div  class="indx  flex-box center indx${+i+1}">
              ${i>=0&&i<3?'<img src="./assets/t'+(i+1) +'.png" />':i+1+ '<span class="ths">th</span>' }

                 </div>  */}
htm +=` <div class="rank-item  ball${i} ballListRef animate__animated "

  key="${i}" id="ballList" ref="ballListRef">
     <div class="flip-card ball flex-box animate__animated  animate__bounceInLeft" 
     style="background:url(./assets/${i>2?'bg'+(i+1):'itemBg'}.png) no-repeat;
     background-size:100% ;
  -webkit-background-size:100% ;
  -moz-background-size:100% ;
  -o-background-size:100% ;
     ">

            <div class="box-left flip-card-front center flex-box center" >           
            ${i<=2?'<img src="./assets/t'+(i+1)+'.png" alt="" />':''} 
            </div>   
            <div class="box-right flip-card-back flex-box between">
                <div class="ball  center  flex-box animate__animated flex">
                  
                    <img src="./assets/${el.mc}.png" alt="" />
                </div>
            
              <div class="time flex-box center">${el.time||"2024-06-06 '"}</div>
            </div>
       </div>
  
</div>
`
//  <div class="name">${i>2?'NO':FiltersStr[i]}</div>
})
rank.html(htm)
let tim = 0
console.log("reslu",data)

$('.time').each(res=>{
let  nums = +$('.time').eq(res).text()
if(Number(nums)){


$('.time').eq(res).animate({
  'counter': nums
}, {
  duration: 5000,
  step:function () {
       $('.time').eq(res).text( (+(this.counter)).toFixed(2).replace('.',"’") );
  }
});
}else{ 
// 异常卡球 非数字时

}
// setTimeout(_=>{
//   $('.time').eq(res).text( nums );
// },5000)
})

cb&&cb()
})
} 
// renderFn(datalist)