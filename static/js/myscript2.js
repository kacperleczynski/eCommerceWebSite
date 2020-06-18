var today = new Date();
var hourNow = today.getHours();
var greeting;

if (hourNow > 16){
  greeting = 'Dobry wieczór!';
} else if ( hourNow > 12 ){
  greeting = 'Dzień dobry!';
} else if ( hourNow > 0 ){
  greeting = 'Dzień dobry!';
} else {
  greeting = 'Witamy!';
}

document.write('<h3 style="color: white;">' + greeting + '</h3>')

