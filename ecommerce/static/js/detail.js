var MainImg = document.getElementById("main-img");
var SmallImg = document.getElementsByClassName("small-img");

// to replace small img with main img
SmallImg[0].onclick = function () {
  MainImg.src = SmallImg[0].src;
}; // if the image is clicked, then a functions runs that changes the  source file with the main img
SmallImg[1].onclick = function () {
  MainImg.src = SmallImg[1].src;
};
SmallImg[2].onclick = function () {
  MainImg.src = SmallImg[2].src;
};
SmallImg[3].onclick = function () {
  MainImg.src = SmallImg[3].src;
};
