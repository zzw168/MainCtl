/*珠子  新版james 或者根据运动卡返回的数据长度为球数量  <img src="./img${QueryParams('ball')||aArr.length||10}/${i+1}.png" /> */
/*socket prot1  9999   prot2 8888*/

let _config = {
    rankConfig:{
        port:9999,
        test:0
    },
    sd:8,
    jiesuanConfg:{
        port:8888,
   
        test:0,
        // 右边数据 赛道 长度
        rtxt1:'2,100 CM',//长度
        rtxt2:16,//赛道障碍
        rtxt3:8,//球
        rtxt4:1,//圈数
        rTopTxt:'MAP DESERT' 
    },
    ip:'127.0.0.1',
    
}
let {jiesuanConfg,rankConfig} = _config

if(QueryParams('sd')) _config.sd = QueryParams('sd')
if(QueryParams('ip')) _config.ip = QueryParams('ip')
if(QueryParams('len')) jiesuanConfg.rtxt1 = QueryParams('len')
if(QueryParams('truns')) jiesuanConfg.rtxt2 = QueryParams('truns')
if(QueryParams('qiu')) jiesuanConfg.rtxt3 = QueryParams('qiu')
if(QueryParams('laps')) jiesuanConfg.rtxt4 = QueryParams('laps')
if(QueryParams('test')){
jiesuanConfg.test = QueryParams('test')
rankConfig.test = QueryParams('test')
}
console.log("rankConfigrankConfig",QueryParams(),rankConfig,_config.sd)