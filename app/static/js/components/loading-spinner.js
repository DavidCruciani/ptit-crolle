export default {
    name: 'LoadingSpinner',
    props: {
        active: { type: Boolean, default: false },
        text: { type: String, default: 'Loading...' },
        overlay: { type: Boolean, default: false }
    },
    template: `
        <transition name="fade">
            <div v-if="active" 
                 :class="overlay ? 'spinner-overlay' : 'spinner-centered'" 
                 class="text-center d-flex flex-column align-items-center justify-content-center">
                
                <div class="position-relative d-flex align-items-center justify-content-center">
                    <div class="spinner-border text-primary" 
                         role="status" 
                         style="width: 3.5rem; height: 3.5rem;">
                    </div>
                    <div class="position-absolute" style="opacity: 0.2;">
                         <div class="spinner-border text-primary" style="width: 3.5rem; height: 3.5rem; animation: none; opacity: 0.3;"></div>
                    </div>
                </div>
                
                <p v-if="text" 
                   class="mt-4 fw-light text-uppercase tracking-wider" 
                   style="color: var(--text-main); letter-spacing: 2px; font-size: 0.85rem;">
                   [[ text ]]
                </p>
            </div>
        </transition>
    `,
    delimiters: ['[[', ']]']
};