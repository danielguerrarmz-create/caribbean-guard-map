/* The only script on the site. The live Squarespace build ships about 913 KB of
   JavaScript; nothing here needs more than a menu toggle.

   The live burger button has no aria-expanded, no aria-controls, and both of its
   label spans carry the hidden attribute, so before its bundle runs a screen
   reader announces "button" with no name at all. This one is labelled and
   reports its own state. */
(function () {
  var btn = document.querySelector(".menu-btn");
  var nav = document.getElementById("nav-main");
  if (!btn || !nav) return;

  function setOpen(open) {
    nav.classList.toggle("open", open);
    btn.setAttribute("aria-expanded", open ? "true" : "false");
    btn.querySelector(".menu-label").textContent = open ? "Cerrar" : "Menú";
  }

  btn.addEventListener("click", function () {
    setOpen(btn.getAttribute("aria-expanded") !== "true");
  });

  // Escape closes and returns focus to the control that opened it, otherwise a
  // keyboard user is stranded inside the drawer.
  document.addEventListener("keydown", function (e) {
    if (e.key === "Escape" && btn.getAttribute("aria-expanded") === "true") {
      setOpen(false);
      btn.focus();
    }
  });

  // A resize past the desktop breakpoint leaves the drawer class on and the
  // button reporting expanded when the drawer is no longer what is showing.
  var mq = window.matchMedia("(min-width:900px)");
  (mq.addEventListener ? mq.addEventListener.bind(mq, "change") : mq.addListener.bind(mq))(
    function (e) { if (e.matches) setOpen(false); }
  );
})();
