/* jshint esversion: 6 */
/* jshint node: true */
'use strict';

async function getDefinition(word) {
    const url = `https://googledictionaryapi.eu-gb.mybluemix.net/?define=${word}`;

    return fetch(url)
        .then(response => response.json());
}

const DIFFBOT_TOKEN = '97862394687c89dfbfd6ed7a979c5806';

async function getArticle(articleUrl) {
  const url = `https://api.diffbot.com/v3/article?token=${DIFFBOT_TOKEN}&url=${encodeURIComponent(articleUrl)}`;

  return fetch(url)
    .then(response => response.json());
}

const startListen = document.querySelector('#listen');
const cancelListen = document.querySelector('#cancelListen');

startListen.onclick = () => {
    const text = document.querySelector('#title').innerText 
                + ' by ' 
                + document.querySelector('#author').innerText
                + '. '
                + document.querySelector('#article').innerText;

    const onend = () => {
        startListen.style.display = '';
        cancelListen.style.display = 'none';
    };

    responsiveVoice.speak(text, 'US English Female', { onend: onend });

    startListen.style.display = 'none';
    cancelListen.style.display = '';
};


cancelListen.onclick = () => {
    responsiveVoice.cancel();

    startListen.style.display = '';
    cancelListen.style.display = 'none';
};

document.querySelector('#removeClutter').onclick = () => {
    responsiveVoice.cancel();

    const url = document.querySelector('#url').value;
  
    const resultSel = document.querySelector('#result_article');
    const loadingSel = document.querySelector('#loading_article');
    const errorSel = document.querySelector('#error_article');
  
    resultSel.style.display = 'none';
    loadingSel.style.display = '';
    errorSel.style.display = 'none';
  
    getArticle(url)
      .then((data) => {
        resultSel.style.display = '';
        loadingSel.style.display = 'none';
        errorSel.style.display = 'none';
  
        document.querySelector('#title').innerText = data.objects[0].title;
        document.querySelector('#source').innerText = data.objects[0].siteName || '';
        document.querySelector('#source').href = data.objects[0].pageUrl;
        document.querySelector('#author').innerText = data.objects[0].author || '';
        document.querySelector('#article').innerHTML = data.objects[0].html;

        startListen.style.display = '';
        cancelListen.style.display = 'none';
      })
      .catch((err) => {
        resultSel.style.display = 'none';
        loadingSel.style.display = 'none';
        errorSel.style.display = '';
      });
  };

document.querySelector('#lookup').onclick = () => {
    const word = document.getElementById('word').value;

    const resultSel = document.querySelector('#result_definition');
    const loadingSel = document.querySelector('#loading_definition');
    const errorSel = document.querySelector('#error_definition');

    resultSel.style.display = 'none';
    loadingSel.style.display = '';
    errorSel.style.display = 'none';

    getDefinition(word)
      .then((data) => {
        resultSel.style.display = '';
        loadingSel.style.display = 'none';
        errorSel.style.display = 'none';

        let word_classes = ['infinitive marker','noun','verb','adjective','adverb','pronoun','preposition','conjunction','determiner','exclamation'];
        
        resultSel.innerHTML = '';
        
        for (let word_class of word_classes) {
            let word_type = data.meaning[word_class];

            if (word_type) {
                const wordMeaning = document.createElement('p');
                const typeDiv = document.createElement('span');
                typeDiv.classList.add('font-weight-bold');
                const meaningDiv = document.createElement('span');
                const br = document.createElement('br');

                let meaning = word_type[0].definition;

                typeDiv.innerHTML = word_class;
                meaningDiv.innerHTML = meaning;
                
                wordMeaning.appendChild(typeDiv);
                wordMeaning.appendChild(br);
                wordMeaning.appendChild(meaningDiv);
                resultSel.appendChild(wordMeaning);
            }
        }
      })
      .catch((err) => {
        console.log(err);
        resultSel.style.display = 'none';
        loadingSel.style.display = 'none';
        errorSel.style.display = '';
      });
};

