document.addEventListener('DOMContentLoaded', () => {
    const proofreadBtn = document.getElementById('proofread-btn');

    proofreadBtn.addEventListener('click', async () => {
        const recipient = document.getElementById('recipient').value;
        const inputText = document.getElementById('input-text').value;

        if (!recipient) {
            alert('送信相手を選択してください。');
            return;
        }

        if (!inputText.trim()) {
            alert('校正したい文章を入力してください。');
            return;
        }

        // ボタン処理中の無効化
        proofreadBtn.disabled = true;
        proofreadBtn.textContent = '処理中...';

        try {
            const response = await fetch('/proofread', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ recipient, preset: 'friend', text: inputText })
            });

            const data = await response.json();
            if (response.ok) {
                document.getElementById('output-text').value = data.result;
            } else {
                alert('エラー: ' + (data.error || 'サーバーエラー'));
            }
        } catch (error) {
            console.error('Error:', error);
            alert('サーバーとの通信に失敗しました。');
        } finally {
            proofreadBtn.disabled = false;
            proofreadBtn.textContent = '検査';
        }
    });
});
