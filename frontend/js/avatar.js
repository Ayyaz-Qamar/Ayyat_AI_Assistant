import * as THREE from 'three';
import { GLTFLoader } from 'three/addons/loaders/GLTFLoader.js';

let scene, camera, renderer, model, mixer;
let clock = new THREE.Clock();

function initAvatar() {
    const container = document.getElementById('orbCanvas').parentElement;
    
    // Hide the old orb canvas
    document.getElementById('orbCanvas').style.display = 'none';
    
    // Create new container for 3D
    const avatarDiv = document.createElement('div');
    avatarDiv.id = 'avatarContainer';
    avatarDiv.style.width = '100%';
    avatarDiv.style.height = '100%';
    container.appendChild(avatarDiv);

    // Scene
    scene = new THREE.Scene();
    
    // Camera
    const width = avatarDiv.clientWidth;
    const height = avatarDiv.clientHeight;
    camera = new THREE.PerspectiveCamera(45, width / height, 0.1, 100);
    camera.position.set(0, 1, 4);
    
    // Renderer
    renderer = new THREE.WebGLRenderer({ antialias: true, alpha: true });
    renderer.setSize(width, height);
    renderer.setPixelRatio(window.devicePixelRatio);
    avatarDiv.appendChild(renderer.domElement);
    
    // Lighting
    const ambient = new THREE.AmbientLight(0x00d9ff, 0.5);
    scene.add(ambient);
    
    const directional = new THREE.DirectionalLight(0xffffff, 1);
    directional.position.set(2, 5, 5);
    scene.add(directional);
    
    const blueLight = new THREE.PointLight(0x00d9ff, 1, 10);
    blueLight.position.set(-2, 2, 2);
    scene.add(blueLight);
    
    // Load avatar
    const loader = new GLTFLoader();
    loader.load(
        '/static/assets/avatar.glb',
        (gltf) => {
            model = gltf.scene;
            model.position.set(0, -1, 0);
            model.scale.set(0.7, 0.7, 0.7);
            scene.add(model);
            
            // Setup animation if available
            if (gltf.animations && gltf.animations.length > 0) {
                mixer = new THREE.AnimationMixer(model);
                const action = mixer.clipAction(gltf.animations[0]);
                action.play();
            }
            
            console.log('[Avatar] Loaded successfully');
            console.log('[Avatar] Animations available:', gltf.animations.length);
        },
        (progress) => {
            console.log('[Avatar] Loading...', (progress.loaded / progress.total * 100) + '%');
        },
        (error) => {
            console.error('[Avatar] Load error:', error);
            document.getElementById('orbCanvas').style.display = 'block';
        }
    );
    
    // Animation loop
    animate();
    
    // Handle resize
    window.addEventListener('resize', onResize);
}

function animate() {
    requestAnimationFrame(animate);
    const delta = clock.getDelta();
    
    if (mixer) mixer.update(delta);
    
    if (model) {
        // Subtle breathing/sway
        model.rotation.y = Math.sin(Date.now() * 0.0005) * 0.1;
    }
    
    if (renderer && scene && camera) {
        renderer.render(scene, camera);
    }
}

function onResize() {
    const avatarDiv = document.getElementById('avatarContainer');
    if (!avatarDiv) return;
    
    const width = avatarDiv.clientWidth;
    const height = avatarDiv.clientHeight;
    
    camera.aspect = width / height;
    camera.updateProjectionMatrix();
    renderer.setSize(width, height);
}

// Initialize when DOM ready
document.addEventListener('DOMContentLoaded', () => {
    setTimeout(initAvatar, 500);
});