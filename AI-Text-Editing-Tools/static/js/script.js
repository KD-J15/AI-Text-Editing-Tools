document.addEventListener('DOMContentLoaded', () => {
    const proofreadBtn = document.getElementById('proofread-btn');
    const sideMenuItems = document.querySelectorAll('.side-menu ul li');

    // サイドメニュークリック時の動作
    sideMenuItems.forEach(item => {
        item.addEventListener('click', () => {
            const recipientInput = document.getElementById('recipient');
            recipientInput.value = item.textContent.trim();
            recipientInput.dataset.preset = item.dataset.preset;
        });
    });

    proofreadBtn.addEventListener('click', async () => {
        const recipient = document.getElementById('recipient').value;
        const inputText = document.getElementById('input-text').value;
        const preset = document.getElementById('recipient').dataset.preset || 'friend';

        if (!recipient.trim()) {
            alert('送信相手を指定してください。');
            return;
        }

        if (!inputText.trim()) {
            alert('校正したい文章を入力してください。');
            return;
        }

        // ボタンを無効化
        proofreadBtn.disabled = true;
        proofreadBtn.textContent = '処理中...';

        try {
            const response = await fetch('/proofread', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({ recipient, preset, text: inputText })
            });

            const data = await response.json();
            if (response.ok) {
                document.getElementById('output-text').value = data.result;
            } else {
                alert(data.error || 'エラーが発生しました。');
            }
        } catch (error) {
            console.error(error);
            alert('サーバーへの接続に失敗しました。');
        } finally {
            // ボタンを再有効化
            proofreadBtn.disabled = false;
            proofreadBtn.textContent = '検査';
        }
    });
});
