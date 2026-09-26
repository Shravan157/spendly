document.addEventListener('DOMContentLoaded', function() {
    const accountTrigger = document.getElementById('account-trigger');
    const accountModal = document.getElementById('account-modal');
    const closeAccount = document.getElementById('close-account');

    if (accountTrigger && accountModal && closeAccount) {
        accountTrigger.addEventListener('click', function() {
            accountModal.style.display = 'flex';
            document.body.style.overflow = 'hidden';
        });

        closeAccount.addEventListener('click', function() {
            accountModal.style.display = 'none';
            document.body.style.overflow = 'auto';
        });

        window.addEventListener('click', function(e) {
            if (e.target === accountModal.querySelector('.modal-overlay')) {
                closeAccount.click();
            }
        });
    }
});
