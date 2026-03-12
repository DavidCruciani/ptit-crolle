export default {
    name: 'OrbitalLoader',
    props: {
        active: { type: Boolean, default: false },
        text: { type: String, default: 'Loading...' }
    },
    template: `
        <transition name="fade">
            <div v-if="active" class="orbital-overlay">
                <div class="orbital-container">
                    <div class="orbital-ring"></div>
                    <div class="orbital-dot"></div>
                    <div class="orbital-text">[[ text ]]</div>
                </div>
            </div>
        </transition>
    `,
    delimiters: ['[[', ']]']
};