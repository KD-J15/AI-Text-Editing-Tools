document.addEventListener('DOMContentLoaded', () => {
    // 既存のコード
    const proofreadBtn = document.getElementById('proofread-btn');
    const inputText = document.getElementById('input-text');
    const charCount = document.getElementById('char-count');
    const maxChars = 1000;
    const resetBtn = document.getElementById('reset-btn'); // リセットボタンを取得

    // リセットボタンの動作を定義
    resetBtn.addEventListener('click', () => {
        inputText.value = ''; // 入力欄をクリア
        charCount.textContent = '0'; // 文字数を0にリセット
    });

    // 文字カウントのリアルタイム更新
    inputText.addEventListener('input', function () {
        const currentLength = inputText.value.length;
        charCount.textContent = currentLength;

        // 1000文字を超えた場合は文字を切り捨て
        if (currentLength > maxChars) {
            inputText.value = inputText.value.substring(0, maxChars);
            charCount.textContent = maxChars;
        }
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
