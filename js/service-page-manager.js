/**
 * Service Page Manager
 * Handles editable content for service pages.
 * Requires: admin-shared.js
 */
const ServicePageManager = {
    pageKey: window.location.pathname.split('/').pop(), // e.g., 'dantu-implantavimas.html'
    init: function () {
        this.loadContent();
        this.injectAdminUI();
        // Listen for login/logout events
        document.addEventListener('adminLoggedIn', () => this.checkAuth());
        document.addEventListener('adminTriggerClicked', () => this.openEditModal());
        this.checkAuth();
    },
    // Load content from localStorage
    loadContent: function () {
        const savedData = localStorage.getItem(`serviceData_${this.pageKey}`);
        if (savedData) {
            const data = JSON.parse(savedData);
            for (const [id, content] of Object.entries(data)) {
                const element = document.getElementById(id);
                if (element) {
                    element.innerHTML = content;
                }
            }
        }
    },
    // Check auth and show/hide admin controls
    checkAuth: function () {
        // The trigger button is handled by admin-shared.js
        // We just need to ensure we are ready to edit
    },
    // Inject the Edit Modal (hidden by default)
    injectAdminUI: function () {
        if (document.getElementById('service-edit-modal')) return;
        const modalHtml = `
        <div id="service-edit-modal" class="fixed inset-0 bg-black bg-opacity-50 hidden items-center justify-center z-[100]">
            <div class="bg-white p-8 rounded-xl shadow-2xl w-full max-w-2xl relative max-h-[90vh] overflow-y-auto">
                <button id="close-service-edit" class="absolute top-4 right-4 text-gray-500 hover:text-gray-700">
                    <i class="fas fa-times text-xl"></i>
                </button>
                <h2 class="text-2xl font-bold text-gray-800 mb-6"><i class="fas fa-edit mr-2 text-blue-500"></i>Redaguoti Puslapį</h2>
                <form id="service-edit-form" class="space-y-6">
                    <div id="editable-fields-container" class="space-y-4">
                        <!-- Fields injected here -->
                    </div>
                    <div class="flex gap-4 pt-4 border-t">
                        <button type="submit" class="flex-1 bg-blue-600 text-white py-3 rounded-lg hover:bg-blue-700 transition font-bold">
                            <i class="fas fa-save mr-2"></i>Išsaugoti Pakeitimus
                        </button>
                    </div>
                </form>
            </div>
        </div>`;
        document.body.insertAdjacentHTML('beforeend', modalHtml);
        // Event Listeners
        document.getElementById('close-service-edit').addEventListener('click', () => {
            document.getElementById('service-edit-modal').classList.add('hidden');
            document.getElementById('service-edit-modal').classList.remove('flex');
        });
        document.getElementById('service-edit-form').addEventListener('submit', (e) => {
            e.preventDefault();
            this.saveContent();
        });
    },
    // Open Edit Modal and populate fields
    openEditModal: function () {
        const container = document.getElementById('editable-fields-container');
        container.innerHTML = '';
        const editableElements = document.querySelectorAll('[data-editable]');
        if (editableElements.length === 0) {
            container.innerHTML = '<p class="text-gray-500 italic">Šiame puslapyje nėra redaguojamų elementų.</p>';
        } else {
            editableElements.forEach(el => {
                const id = el.id;
                const label = el.dataset.label || id;
                const isTextarea = el.dataset.type === 'textarea' || el.tagName === 'P' || el.tagName === 'DIV';
                const value = el.innerHTML.trim(); // Use innerHTML to preserve basic formatting like <br>
                let inputHtml = '';
                if (isTextarea) {
                    inputHtml = `<textarea name="${id}" rows="4" class="w-full border rounded-lg px-3 py-2 focus:ring-2 focus:ring-blue-500">${value}</textarea>`;
                } else {
                    inputHtml = `<input type="text" name="${id}" value="${value.replace(/"/g, '&quot;')}" class="w-full border rounded-lg px-3 py-2 focus:ring-2 focus:ring-blue-500">`;
                }
                const fieldHtml = `
                <div>
                    <label class="block text-sm font-bold text-gray-700 mb-1 capitalize">${label}</label>
                    ${inputHtml}
                </div>`;
                container.insertAdjacentHTML('beforeend', fieldHtml);
            });
        }
        const modal = document.getElementById('service-edit-modal');
        modal.classList.remove('hidden');
        modal.classList.add('flex');
    },
    // Save content to localStorage and update DOM
    saveContent: function () {
        const form = document.getElementById('service-edit-form');
        const formData = new FormData(form);
        const data = {};
        for (const [id, value] of formData.entries()) {
            data[id] = value;
            const element = document.getElementById(id);
            if (element) {
                element.innerHTML = value;
            }
        }
        localStorage.setItem(`serviceData_${this.pageKey}`, JSON.stringify(data));
        // Close modal
        const modal = document.getElementById('service-edit-modal');
        modal.classList.add('hidden');
        modal.classList.remove('flex');
        alert('Pakeitimai išsaugoti!');
    }
};
// Initialize on load
document.addEventListener('DOMContentLoaded', () => {
    ServicePageManager.init();
});
