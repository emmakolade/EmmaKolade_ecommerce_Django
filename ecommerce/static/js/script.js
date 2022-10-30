const bar = document.getElementById("bar");
const close = document.getElementById("close-side");
const nav = document.getElementById("navbar");

// to check if the navbar is showing in the screen or not
if (bar) {
  bar.addEventListener("click", () => {
    nav.classList.add('activee');
  });
}

// to make the xmark button clickable
if (close) {
  close.addEventListener("click", () => {
    nav.classList.remove("activee");
  });
}