const ADMIN_PASSWORD = "admin";
/**
 * Shared Admin Utilities
 */
const AdminShared = {
    // Check if user is logged in
    isLoggedIn: function () {
        return localStorage.getItem('isLoggedIn') === 'true';
    },
    // Login function
    login: function (password) {
        if (password === ADMIN_PASSWORD) {
            localStorage.setItem('isLoggedIn', 'true');
            return true;
        }
        return false;
    },
    // Logout function
    logout: function () {
        localStorage.removeItem('isLoggedIn');
        window.location.reload();
    },
    // Inject Login Modal into the DOM
    injectLoginModal: function () {
        if (document.getElementById('admin-login-modal')) return;
        const modalHtml = `
        <div id="admin-login-modal" class="fixed inset-0 bg-black bg-opacity-50 hidden items-center justify-center z-[100]">
            <div class="bg-white p-8 rounded-xl shadow-2xl w-full max-w-md relative">
                <button id="close-login-btn" class="absolute top-4 right-4 text-gray-500 hover:text-gray-700">
                    <i class="fas fa-times text-xl"></i>
                </button>
                <div class="text-center mb-8">
                    <i class="fas fa-lock text-4xl text-blue-500 mb-4"></i>
                    <h2 class="text-2xl font-bold text-gray-800">Prisijungimas</h2>
                    <p class="text-gray-500">Administratoriaus teisės</p>
                </div>
                <form id="login-form" class="space-y-6">
                    <div>
                        <label class="block text-gray-700 text-sm font-bold mb-2" for="password">
                            Slaptažodis
                        </label>
                        <input
                            class="shadow appearance-none border rounded w-full py-3 px-4 text-gray-700 leading-tight focus:outline-none focus:shadow-outline focus:border-blue-500"
                            id="password" type="password" placeholder="Įveskite slaptažodį">
                    </div>
                    <button
                        class="w-full bg-blue-500 hover:bg-blue-700 text-white font-bold py-3 px-4 rounded focus:outline-none focus:shadow-outline transition"
                        type="submit">
                        Prisijungti
                    </button>
                    <p id="login-error" class="text-red-500 text-xs italic hidden text-center">Neteisingas slaptažodis.</p>
                </form>
            </div>
        </div>`;
        document.body.insertAdjacentHTML('beforeend', modalHtml);
        // Event Listeners for Modal
        const modal = document.getElementById('admin-login-modal');
        const closeBtn = document.getElementById('close-login-btn');
        const form = document.getElementById('login-form');
        const errorMsg = document.getElementById('login-error');
        closeBtn.addEventListener('click', () => {
            modal.classList.add('hidden');
            modal.classList.remove('flex');
        });
        form.addEventListener('submit', (e) => {
            e.preventDefault();
            const password = document.getElementById('password').value;
            if (this.login(password)) {
                modal.classList.add('hidden');
                modal.classList.remove('flex');
                errorMsg.classList.add('hidden');
                // Trigger a custom event that pages can listen to
                document.dispatchEvent(new CustomEvent('adminLoggedIn'));
                window.location.reload(); // Simple reload to refresh state
            } else {
                errorMsg.classList.remove('hidden');
            }
        });
    },
    // Inject Admin Trigger Button (Lock Icon)
    injectAdminTrigger: function () {
        if (document.getElementById('admin-trigger-btn')) return;
        const btn = document.createElement('button');
        btn.id = 'admin-trigger-btn';
        btn.className = 'fixed bottom-4 right-4 text-gray-400 hover:text-gray-600 bg-white p-2 rounded-full shadow-md z-50 opacity-50 hover:opacity-100 transition';
        btn.innerHTML = '<i class="fas fa-lock"></i>';
        document.body.appendChild(btn);
        btn.addEventListener('click', () => {
            if (this.isLoggedIn()) {
                // If already logged in, maybe scroll to admin panel or show toolbar
                // For now, let's just dispatch an event
                document.dispatchEvent(new CustomEvent('adminTriggerClicked'));
            } else {
                const modal = document.getElementById('admin-login-modal');
                modal.classList.remove('hidden');
                modal.classList.add('flex');
            }
        });
    },
    // Initialize
    init: function () {
        this.injectLoginModal();
        this.injectAdminTrigger();
    }
};
// Auto-init on load
document.addEventListener('DOMContentLoaded', () => {
    AdminShared.init();
});
