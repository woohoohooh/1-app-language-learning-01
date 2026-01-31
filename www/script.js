const Utils = {
  async getAvailableLists() {
    try {
      return ['list_basic_1.json'];
    } catch (error) {
      console.error('Error getting lists:', error);
      return [];
    }
  },

  async loadListData(filename) {
    try {
      const response = await fetch(filename);
      if (!response.ok) throw new Error('Failed to load list');
      let data = await response.json();
      data.filename = filename; // Ensure filename is set
      return WordDB.updateListStatus(data);
    } catch (error) {
      console.error('Error loading list:', error);
      return null;
    }
  },

  shuffleArray(array) {
    const shuffled = [...array];
    for (let i = shuffled.length - 1; i > 0; i--) {
      const j = Math.floor(Math.random() * (i + 1));
      [shuffled[i], shuffled[j]] = [shuffled[j], shuffled[i]];
    }
    return shuffled;
  },

  filterLists(lists, filters) {
    return lists.filter(list => {
      if (filters.level && list.level !== filters.level) return false;
      if (filters.theme && list.theme !== filters.theme) return false;
      return true;
    });
  },

  getUniqueFilters(lists) {
    const levels = new Set();
    const themes = new Set();

    lists.forEach(list => {
      if (list.level) levels.add(list.level);
      if (list.theme) themes.add(list.theme);
    });

    return {
      levels: Array.from(levels).sort(),
      themes: Array.from(themes).sort()
    };
  }
};