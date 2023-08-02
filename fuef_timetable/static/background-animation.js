const background = document.querySelector(".background");
for (var i = 0; i <= 50; i++) {
  const blocks = document.createElement("div");
  blocks.classList.add("block");
  blocks.style.backgroundColor = "#E72659";
  background.appendChild(blocks);
}

let animateBlocks = () => {
  anime({
    targets: ".block",
    translateX: () => {
      return anime.random(-1500, 1500);
    },
    translateY: () => {
      return anime.random(-700, 700);
    },
    scale: () => {
      return anime.random(1, 10);
    },

    easing: "linear",
    duration: 10000,
    complete: animateBlocks
  });
};
animateBlocks();
