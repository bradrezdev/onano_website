import reflex as rx
import json

BRAND_DARK_BLUE = "#22439B",

# Load the configuration from the asset file
try:
    with open("assets/particles_config.json", "r") as f:
        particles_config = json.load(f)
except Exception as e:
    print(f"Error loading particles config: {e}")
    particles_config = {}

def particles_background() -> rx.Component:
    """
    A particle background component using pure Javascript tsparticles.
    Uses plain CDN and script injection to avoid React hydration issues.
    """
    # Serialize config to JSON string for injection
    config_json = json.dumps(particles_config)
    
    return rx.fragment(
        # Load the full bundle (includes physics, shapes, etc)
        rx.script(src="https://cdn.jsdelivr.net/npm/tsparticles@2.12.0/tsparticles.bundle.min.js"),
        
        # Inject Initialization Logic
        rx.script(
            f"""
            const particlesConfig = {config_json};
            
            // Function to check and load particles
            const initParticles = () => {{
                // Prevent multiple running instances if possible
                if (window.particlesInitialized) return;

                const element = document.getElementById("tsparticles");
                const library = window.tsParticles;
                
                if (library && element) {{
                    console.log("DEBUG: Initializing Particles...");
                    library.load("tsparticles", particlesConfig).then((container) => {{
                        console.log("DEBUG: Base Engine Loaded. Injecting Custom Distribution...");
                        
                        // Custom Distribution Logic
                        const dist = particlesConfig.particle_distribution;
                        if (dist && Array.isArray(dist)) {{
                            dist.forEach(group => {{
                                for (let i = 0; i < group.count; i++) {{
                                    container.particles.addParticle(undefined, {{
                                        mass: 10,
                                        size: {{
                                            value: group.size,
                                            random: false 
                                        }}
                                    }});
                                }}
                            }});
                            console.log("DEBUG: Custom Particles Injected Successfully");
                        }}

                        window.particlesInitialized = true;
                    }}).catch(e => console.error("Particles Error:", e));
                }} 
            }};
            
            // Robust Polling Mechanism
            const polling = setInterval(() => {{
                // If it's done, stop polling
                if (window.particlesInitialized) {{
                    clearInterval(polling);
                    return;
                }}
                
                // Try to init
                initParticles();
            }}, 250); // Check every 250ms
            
            // Safety timeout to stop checking after 30 seconds
            setTimeout(() => clearInterval(polling), 30000);
 
            """
        ),
        
        # The container
        rx.box(
            id="tsparticles",
            position="fixed",
            top="0",
            left="0",
            width="100%",
            height="100%",
            z_index="0", # Set to 0 so it sits at the base level
            # The background gradient is applied here, behind the transparent canvas
            bg=f"radial-gradient(circle at center, {BRAND_DARK_BLUE} 0%, #0a1128 100%)",
            style={"pointer_events": "none"} # Allow clicks to pass through initially, config can override
        ),
    )

