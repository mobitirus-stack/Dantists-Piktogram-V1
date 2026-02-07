const ADMIN_PASSWORD = "admin";
document.addEventListener('DOMContentLoaded', () => {
    injectAdminUI();
    loadContent();
});
function injectAdminUI() {
    // 1. Inject Login Modal
    const modalHtml = `
    <div id="admin-login-modal" class="fixed inset-0 bg-black bg-opacity-50 hidden items-center justify-center z-[100]">
        <div class="bg-white p-8 rounded-xl shadow-2xl w-full max-w-md relative">
            <button id="close-login-btn" class="absolute top-4 right-4 text-gray-500 hover:text-gray-700">
                <i class="fas fa-times text-xl"></i>
            </button>
            <div class="text-center mb-8">
                <i class="fas fa-lock text-4xl text-blue-500 mb-4"></i>
                <h2 class="text-2xl font-bold text-gray-800">Prisijungimas</h2>
                <p class="text-gray-500">Puslapio redagavimas</p>
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
    // 2. Inject Admin Toolbar (Hidden by default)
    const toolbarHtml = `
    <div id="admin-toolbar" class="fixed bottom-0 left-0 w-full bg-gray-900 text-white p-4 z-[99] hidden shadow-lg border-t-4 border-blue-500">
        <div class="container mx-auto flex justify-between items-center">
            <div class="flex items-center space-x-4">
                <span class="font-bold text-lg"><i class="fas fa-edit mr-2"></i>Redagavimo režimas</span>
                <span class="text-sm text-gray-400">Spustelėkite bet kurį tekstą, kad jį pakeistumėte.</span>
            </div>
            <div class="flex space-x-4">
                <button id="save-content-btn" class="bg-green-600 hover:bg-green-700 text-white px-6 py-2 rounded font-bold transition">
                    <i class="fas fa-save mr-2"></i>Išsaugoti
                </button>
                <button id="logout-btn" class="bg-red-600 hover:bg-red-700 text-white px-6 py-2 rounded font-bold transition">
                    <i class="fas fa-sign-out-alt mr-2"></i>Atsijungti
                </button>
            </div>
        </div>
    </div>`;
    document.body.insertAdjacentHTML('beforeend', toolbarHtml);
    // 3. Inject Lock Icon in Footer
    // We look for the copyright text or just append to footer if found
    const footer = document.querySelector('footer');
    if (footer) {
        const lockBtn = document.createElement('button');
        lockBtn.id = 'admin-trigger-btn';
        lockBtn.className = 'fixed bottom-4 right-4 text-gray-400 hover:text-gray-600 bg-white p-2 rounded-full shadow-md z-50 opacity-50 hover:opacity-100 transition';
        lockBtn.innerHTML = '<i class="fas fa-lock"></i>';
        document.body.appendChild(lockBtn); // Append to body to be fixed position
        // Event Listeners
        const adminLoginModal = document.getElementById('admin-login-modal');
        const closeLoginBtn = document.getElementById('close-login-btn');
        const loginForm = document.getElementById('login-form');
        const loginError = document.getElementById('login-error');
        const adminToolbar = document.getElementById('admin-toolbar');
        const logoutBtn = document.getElementById('logout-btn');
        const saveContentBtn = document.getElementById('save-content-btn');
        lockBtn.addEventListener('click', () => {
            if (localStorage.getItem('isLoggedIn') === 'true') {
                enableEditing();
            } else {
                adminLoginModal.classList.remove('hidden');
                adminLoginModal.classList.add('flex');
            }
        });
        closeLoginBtn.addEventListener('click', () => {
            adminLoginModal.classList.add('hidden');
            adminLoginModal.classList.remove('flex');
        });
        loginForm.addEventListener('submit', (e) => {
            e.preventDefault();
            const password = document.getElementById('password').value;
            if (password === ADMIN_PASSWORD) {
                localStorage.setItem('isLoggedIn', 'true');
                adminLoginModal.classList.add('hidden');
                adminLoginModal.classList.remove('flex');
                enableEditing();
                loginError.classList.add('hidden');
            } else {
                loginError.classList.remove('hidden');
            }
        });
        logoutBtn.addEventListener('click', () => {
            localStorage.removeItem('isLoggedIn');
            disableEditing();
            window.location.reload();
        });
        saveContentBtn.addEventListener('click', () => {
            saveContent();
            alert('Pakeitimai išsaugoti!');
        });
        // Auto-login check
        if (localStorage.getItem('isLoggedIn') === 'true') {
            enableEditing();
        }
    }
}
function enableEditing() {
    const content = document.getElementById('page-content');
    const toolbar = document.getElementById('admin-toolbar');
    if (content) {
        content.contentEditable = "true";
        content.classList.add('outline-dashed', 'outline-2', 'outline-blue-500', 'p-1');
    }
    if (toolbar) {
        toolbar.classList.remove('hidden');
    }
}
function disableEditing() {
    const content = document.getElementById('page-content');
    const toolbar = document.getElementById('admin-toolbar');
    if (content) {
        content.contentEditable = "false";
        content.classList.remove('outline-dashed', 'outline-2', 'outline-blue-500', 'p-1');
    }
    if (toolbar) {
        toolbar.classList.add('hidden');
    }
}
function getKey() {
    return 'page_content_' + window.location.pathname;
}
function saveContent() {
    const content = document.getElementById('page-content');
    if (content) {
        localStorage.setItem(getKey(), content.innerHTML);
    }
}
function loadContent() {
    const savedContent = localStorage.getItem(getKey());
    const content = document.getElementById('page-content');
    if (savedContent && content) {
        content.innerHTML = savedContent;
    }
}
