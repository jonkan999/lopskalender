export function smoothScrollDown() {
  const currentPosition = window.pageYOffset;
  if (currentPosition < 100) {
    window.scrollBy({
      top: 100 - currentPosition,
      behavior: "smooth",
    });
  }
}
