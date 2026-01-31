const WordDB = {
  saveWordStatus(listId, english, status) {
    const key = `word_${listId}_${english}`;
    localStorage.setItem(key, status);
  },

  getWordStatus(listId, english) {
    const key = `word_${listId}_${english}`;
    return localStorage.getItem(key) || 'new';
  },

  updateListStatus(listData) {
    listData.words.forEach(word => {
      const status = this.getWordStatus(listData.filename, word.english);
      word.status = status;
    });
    return listData;
  },

  getWordsForReview(listData) {
    const reviewedWords = [];
    const newWords = [];

    listData.words.forEach(word => {
      const status = this.getWordStatus(listData.filename, word.english);
      word.status = status;

      if (status === 'review') {
        reviewedWords.push(word);
      } else if (status === 'new') {
        newWords.push(word);
      }
    });

    return [...reviewedWords, ...newWords];
  },

  resetListProgress(listId) {
    const keys = Object.keys(localStorage);
    keys.forEach(key => {
      if (key.startsWith(`word_${listId}_`)) {
        localStorage.removeItem(key);
      }
    });
  },

  getListProgress(listId, totalWords) {
    let known = 0;
    let review = 0;
    let newWords = totalWords;

    const keys = Object.keys(localStorage);
    keys.forEach(key => {
      if (key.startsWith(`word_${listId}_`)) {
        const status = localStorage.getItem(key);
        if (status === 'known') known++;
        if (status === 'review') review++;
      }
    });

    newWords = totalWords - known - review;

    return { known, review, new: newWords };
  }
};