// Переключатель языка и полноэкранный просмотр фото (клавиши, стрелки, свайпы).
(function () {
  var root = document.documentElement;
  var btn = document.querySelector('.lang');
  if (btn) btn.addEventListener('click', function () {
    var l = root.dataset.lang === 'fr' ? 'en' : 'fr';
    root.dataset.lang = l; root.lang = l;
    try { localStorage.setItem('lang', l); } catch (e) {}
  });

  var imgs = [].slice.call(document.querySelectorAll('.ph'));
  var lb = document.querySelector('.lb');
  if (!imgs.length || !lb) return;
  var big = lb.querySelector('img'), cnt = lb.querySelector('.lb-c'), cur = 0;

  function show(i) {
    cur = (i + imgs.length) % imgs.length;
    big.src = imgs[cur].dataset.full;
    big.alt = imgs[cur].alt;
    cnt.textContent = (cur + 1) + ' / ' + imgs.length;
    var pre = new Image(); pre.src = imgs[(cur + 1) % imgs.length].dataset.full;
  }
  function open(i) { show(i); lb.hidden = false; document.body.style.overflow = 'hidden'; }
  function close() { lb.hidden = true; document.body.style.overflow = ''; }

  imgs.forEach(function (im, i) { im.addEventListener('click', function () { open(i); }); });
  lb.querySelector('.lb-x').addEventListener('click', close);
  lb.querySelector('.lb-p').addEventListener('click', function (e) { e.stopPropagation(); show(cur - 1); });
  lb.querySelector('.lb-n').addEventListener('click', function (e) { e.stopPropagation(); show(cur + 1); });
  big.addEventListener('click', function () { show(cur + 1); });
  document.addEventListener('keydown', function (e) {
    if (lb.hidden) return;
    if (e.key === 'Escape') close();
    if (e.key === 'ArrowRight') show(cur + 1);
    if (e.key === 'ArrowLeft') show(cur - 1);
  });
  var x0 = null, y0 = null;
  lb.addEventListener('touchstart', function (e) { x0 = e.touches[0].clientX; y0 = e.touches[0].clientY; }, { passive: true });
  lb.addEventListener('touchend', function (e) {
    if (x0 === null) return;
    var dx = e.changedTouches[0].clientX - x0, dy = e.changedTouches[0].clientY - y0;
    if (Math.abs(dx) > 50 && Math.abs(dx) > Math.abs(dy)) show(cur + (dx < 0 ? 1 : -1));
    else if (dy > 80) close();
    x0 = null;
  }, { passive: true });
})();
