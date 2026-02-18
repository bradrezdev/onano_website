(function() {
    // Variables de estado para la interpolación
    let targetX = 0.5;
    let targetY = 0.5;
    let currentX = 0.5;
    let currentY = 0.5;
    
    // Factor de suavizado (0.01 - 0.1). 
    // Menor número = más suave/lento (más "luxury"). 
    // Mayor número = más reactivo.
    const LERP_FACTOR = 0.05;

    /**
     * Función de Interpolación Lineal (Linear Interpolation)
     * Suaviza el movimiento entre el valor actual y el objetivo.
     */
    function lerp(start, end, factor) {
        return start + (end - start) * factor;
    }

    /**
     * Bucle de animación (Game Loop)
     * Se ejecuta en cada frame disponible del navegador (~60fps).
     */
    function update() {
        // Interpolamos los valores actuales hacia el objetivo
        currentX = lerp(currentX, targetX, LERP_FACTOR);
        currentY = lerp(currentY, targetY, LERP_FACTOR);

        // Actualizamos las variables CSS globales
        document.documentElement.style.setProperty('--mouse-x', currentX);
        document.documentElement.style.setProperty('--mouse-y', currentY);

        // Solicitamos el siguiente frame
        requestAnimationFrame(update);
    }

    /**
     * Manejador de eventos de movimiento
     */
    const onMove = (x, y) => {
        // Normalizamos coordenadas de 0 a 1
        targetX = x / window.innerWidth;
        targetY = y / window.innerHeight;
    };

    // Event listeners globales (window) para capturar movimiento en toda la app
    window.addEventListener('mousemove', (e) => onMove(e.clientX, e.clientY));
    
    // Soporte para touch (móviles/tablets)
    window.addEventListener('touchmove', (e) => {
        if(e.touches.length > 0) {
            onMove(e.touches[0].clientX, e.touches[0].clientY);
        }
    }, { passive: true });

    // Iniciar el bucle de animación
    update();
})();