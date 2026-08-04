/* ============================================
   Charlotte 个人网站 · 骨架 JS（占位版）
   1) Three.js：第一屏 3D 场景（旋转线框 + 鼠标视差）
   2) GSAP + ScrollTrigger：区块入场动画
   K3 设计稿落地后，此处替换为最终交互方案
   ============================================ */

(() => {
  const canvas = document.getElementById('hero-3d');
  if (!canvas) return;

  /* ---------- Three.js 第一屏 ---------- */
  const renderer = new THREE.WebGLRenderer({ canvas, antialias: true, alpha: true });
  renderer.setPixelRatio(Math.min(window.devicePixelRatio, 2));
  renderer.setSize(window.innerWidth, window.innerHeight);

  const scene = new THREE.Scene();
  const camera = new THREE.PerspectiveCamera(60, window.innerWidth / window.innerHeight, 0.1, 100);
  camera.position.z = 6;

  // 占位物体：旋转线框二十面体 + 环绕粒子
  const geo = new THREE.IcosahedronGeometry(1.6, 1);
  const mat = new THREE.MeshBasicMaterial({ color: 0x7c6cff, wireframe: true });
  const mesh = new THREE.Mesh(geo, mat);
  scene.add(mesh);

  const particleCount = 400;
  const pGeo = new THREE.BufferGeometry();
  const positions = new Float32Array(particleCount * 3);
  for (let i = 0; i < particleCount * 3; i += 3) {
    positions[i]     = (Math.random() - 0.5) * 20;
    positions[i + 1] = (Math.random() - 0.5) * 20;
    positions[i + 2] = (Math.random() - 0.5) * 20;
  }
  pGeo.setAttribute('position', new THREE.BufferAttribute(positions, 3));
  const pMat = new THREE.PointsMaterial({ color: 0xffffff, size: 0.04, transparent: true, opacity: 0.6 });
  const particles = new THREE.Points(pGeo, pMat);
  scene.add(particles);

  // 鼠标视差（目标角度）
  let mouseX = 0, mouseY = 0;
  window.addEventListener('pointermove', (e) => {
    mouseX = (e.clientX / window.innerWidth - 0.5) * 2;
    mouseY = (e.clientY / window.innerHeight - 0.5) * 2;
  }, { passive: true });

  function animate(time) {
    mesh.rotation.x += 0.003;
    mesh.rotation.y += 0.005;
    particles.rotation.y += 0.0008;

    // 平滑跟随鼠标
    mesh.rotation.y += (mouseX * 0.5 - mesh.rotation.y) * 0.02;
    mesh.rotation.x += (-mouseY * 0.4 - mesh.rotation.x) * 0.02;

    renderer.render(scene, camera);
    requestAnimationFrame(animate);
  }
  animate();

  /* ---------- 自适应 ---------- */
  window.addEventListener('resize', () => {
    camera.aspect = window.innerWidth / window.innerHeight;
    camera.updateProjectionMatrix();
    renderer.setSize(window.innerWidth, window.innerHeight);
  });

  /* ---------- GSAP 入场动画（占位） ---------- */
  gsap.registerPlugin(ScrollTrigger);

  // 第一屏文字浮现
  gsap.from('.hero-name', { opacity: 0, y: 30, duration: 1, ease: 'power2.out', delay: 0.3 });
  gsap.from('.hero-tagline', { opacity: 0, y: 20, duration: 1, ease: 'power2.out', delay: 0.6 });
  gsap.from('.scroll-hint', { opacity: 0, duration: 1, delay: 1.2 });

  // 滚动提示呼吸动画
  gsap.to('.scroll-hint', { y: 8, repeat: -1, yoyo: true, duration: 0.9, ease: 'sine.inOut' });

  // 各区块入场：向上淡入
  gsap.utils.toArray('.section, .learning-bar').forEach((el) => {
    gsap.from(el, {
      opacity: 0,
      y: 40,
      duration: 0.9,
      ease: 'power2.out',
      scrollTrigger: { trigger: el, start: 'top 85%' },
    });
  });
})();
