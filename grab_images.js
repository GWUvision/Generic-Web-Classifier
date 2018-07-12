// // pull down jquery into the JavaScript console
// var script = document.createElement('script');
// script.src = "https://ajax.googleapis.com/ajax/libs/jquery/2.2.0/jquery.min.js";
// document.getElementsByTagName('head')[0].appendChild(script);
//
// // grab the URLs
// var urls = $('.rg_di .rg_meta').map(function() { return JSON.parse($(this).text()).ou; });
//
// // write the URls to file (one per line)
// var textToSave = urls.toArray().join('\n');
// var hiddenElement = document.createElement('a');
// hiddenElement.href = 'data:attachment/text,' + encodeURI(textToSave);
// hiddenElement.target = '_blank';
// hiddenElement.download = 'urls.txt';
// hiddenElement.click();

var Scraper = require ('images-scraper')
  , bing = new Scraper.Bing();

bing.list({
    keyword: 'banana',
    num: 10,
    detail: true
})
.then(function (res) {
    console.log('first 10 results from bing', res);
}).catch(function(err) {
    console.log('err',err);
})
