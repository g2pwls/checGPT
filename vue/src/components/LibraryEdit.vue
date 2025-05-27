<template>
  <div class="library-edit">
    <h2 class="section-title">내 서재 관리</h2>
    <div class="top-books-section">
      <h3>대표 도서 선택</h3>
      <p class="description">가장 좋아하는 책 3권을 선택해주세요 (1순위부터 3순위까지)</p>
      
      <div class="top-books-grid">
        <div v-for="(rank, index) in 3" :key="rank" class="rank-slot">
          <div class="rank-number">{{ rank }}순위</div>
          <div v-if="topBooks[index]" class="selected-book">
            <img :src="topBooks[index].book.cover" :alt="topBooks[index].book.title" class="book-cover">
            <div class="book-info">
              <h4>{{ topBooks[index].book.title }}</h4>
              <p>{{ topBooks[index].book.author }}</p>
            </div>
            <button class="remove-btn" @click="removeTopBook(index)">×</button>
          </div>
          <div v-else class="empty-slot">
            <span>선택된 책이 없습니다</span>
          </div>
        </div>
      </div>
    </div>

    <div class="library-grid">
      <div v-for="item in library" :key="item.id" 
           class="library-item" 
           :class="{ 'selected': isTopBook(item) }"
           @click="selectTopBook(item)">
        <div class="book-cover-container">
          <img :src="item.book.cover" :alt="item.book.title" class="book-cover">
        </div>
        <h3 class="book-title">{{ item.book.title }}</h3>
        <p class="book-author">{{ item.book.author }}</p>
      </div>
    </div>

    <div class="action-buttons">
      <button class="save-btn" @click="saveTopBooks">저장하기</button>
      <button class="cancel-btn" @click="$emit('close')">취소</button>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import axios from 'axios'

const props = defineProps({
  library: {
    type: Array,
    required: true
  }
})

const emit = defineEmits(['close', 'update'])

const topBooks = ref([])

const isTopBook = (book) => {
  return topBooks.value.some(topBook => topBook.id === book.id)
}

const selectTopBook = (book) => {
  // 이미 선택된 책인 경우 제거
  const existingIndex = topBooks.value.findIndex(topBook => topBook.id === book.id)
  if (existingIndex !== -1) {
    topBooks.value.splice(existingIndex, 1)
    return
  }

  // 3개 이상 선택된 경우 첫 번째 책 제거
  if (topBooks.value.length >= 3) {
    topBooks.value.shift()
  }

  // 새 책 추가
  topBooks.value.push(book)
}

const removeTopBook = (index) => {
  topBooks.value.splice(index, 1)
}

const saveTopBooks = async () => {
  try {
    const token = localStorage.getItem('token')
    const response = await axios.post(
      'http://127.0.0.1:8000/api/users/top-books/',
      {
        top_books: topBooks.value.map(book => book.book.id)
      },
      {
        headers: {
          Authorization: `Token ${token}`
        }
      }
    )
    
    emit('update')
    emit('close')
  } catch (error) {
    console.error('Error saving top books:', error)
    if (error.response?.status === 400) {
      alert(error.response.data.error || '대표 도서 저장에 실패했습니다.')
    } else {
      alert('대표 도서 저장에 실패했습니다.')
    }
  }
}

onMounted(async () => {
  try {
    const token = localStorage.getItem('token')
    const response = await axios.get(
      'http://127.0.0.1:8000/api/users/top-books/',
      {
        headers: {
          Authorization: `Token ${token}`
        }
      }
    )
    topBooks.value = response.data
  } catch (error) {
    console.error('Error loading top books:', error)
  }
})
</script>

<style scoped>
.library-edit {
  padding: 20px;
  background-color: #ffffff;
  border-radius: 8px;
  box-shadow: 0 2px 5px rgba(0, 0, 0, 0.05);
  border: 1px solid #ddd;
  font-family: 'Noto Sans KR', sans-serif;
  color: #333;
}

.section-title {
  font-size: 1.5rem;
  font-weight: bold;
  margin-bottom: 20px;
  color: #333;
  padding-bottom: 10px;
  border-bottom: 1px solid #eee;
}

.top-books-section {
  margin-bottom: 20px;
}

.description {
  color: #777;
  margin-bottom: 15px;
  font-size: 0.95rem;
}

.top-books-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(150px, 1fr));
  gap: 20px;
  margin-bottom: 20px;
}

.rank-slot {
  background-color: #f9f9f9;
  border-radius: 8px;
  padding: 15px;
  min-height: 220px;
  position: relative;
  border: 1px solid #eee;
}

.rank-number {
  position: absolute;
  top: 10px;
  left: 10px;
  background-color: #333;
  color: white;
  font-size: 0.8rem;
  padding: 4px 8px;
  border-radius: 12px;
}

.selected-book {
  display: flex;
  flex-direction: column;
  align-items: center;
  height: 100%;
  gap: 10px;
}

.empty-slot {
  display: flex;
  align-items: center;
  justify-content: center;
  height: 100%;
  color: #777;
  font-size: 0.9rem;
}

.book-cover {
  width: 100px;
  height: 150px;
  object-fit: cover;
  border-radius: 4px;
  margin-bottom: 10px;
  border: 1px solid #ddd;
}

.book-info {
  text-align: center;
}

.book-info h4 {
  font-size: 1rem;
  font-weight: bold;
  margin-bottom: 4px;
  color: #333;
}

.book-info p {
  font-size: 0.9rem;
  color: #777;
}

.remove-btn {
  position: absolute;
  top: 10px;
  right: 10px;
  background-color: #dc3545;
  color: white;
  border: none;
  border-radius: 50%;
  width: 24px;
  height: 24px;
  display: flex;
  align-items: center;
  justify-content: center;
  cursor: pointer;
  font-size: 1.2rem;
  transition: background-color 0.2s ease;
}

.remove-btn:hover {
  background-color: #c82333;
}

.library-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(120px, 1fr));
  gap: 15px;
  margin-bottom: 20px;
}

.library-item {
  background-color: #f9f9f9;
  border-radius: 8px;
  padding: 10px;
  transition: all 0.2s ease;
  cursor: pointer;
  box-shadow: 0 1px 3px rgba(0, 0, 0, 0.03);
  display: flex;
  flex-direction: column;
  align-items: center;
  text-align: center;
  border: 1px solid #eee;
}

.library-item:hover {
  transform: translateY(-2px);
  box-shadow: 0 3px 6px rgba(0, 0, 0, 0.06);
}

.library-item.selected {
  border-color: #333;
  box-shadow: 0 2px 5px rgba(0, 0, 0, 0.1);
}

.library-item .book-cover-container {
  width: 80px;
  height: 120px;
  margin: 0 auto 8px;
}

.library-item .book-cover {
  width: 100%;
  height: 100%;
  object-fit: cover;
  border-radius: 4px;
  border: 1px solid #ddd;
}

.library-item .book-title {
  font-size: 0.9rem;
  font-weight: bold;
  margin-bottom: 4px;
  color: #333;
  word-break: keep-all;
}

.library-item .book-author {
  font-size: 0.8rem;
  color: #777;
}

.action-buttons {
  display: flex;
  justify-content: flex-end;
  gap: 10px;
  margin-top: 20px;
}

.save-btn,
.cancel-btn {
  padding: 10px 20px;
  border: none;
  border-radius: 4px;
  cursor: pointer;
  font-size: 1rem;
  transition: background-color 0.2s ease;
}

.save-btn {
  background-color: #333;
  color: white;
}

.save-btn:hover {
  background-color: #555;
}

.cancel-btn {
  background-color: #eee;
  color: #333;
  border: 1px solid #ddd;
}

.cancel-btn:hover {
  background-color: #ddd;
}

@media (max-width: 768px) {
  .library-edit {
    padding: 15px;
  }

  .section-title {
    font-size: 1.3rem;
  }

  .top-books-grid {
    grid-template-columns: repeat(auto-fill, minmax(120px, 1fr));
    gap: 15px;
  }

  .rank-slot {
    padding: 10px;
    min-height: 180px;
  }

  .book-cover {
    width: 80px;
    height: 120px;
  }

  .library-grid {
    grid-template-columns: repeat(auto-fill, minmax(100px, 1fr));
    gap: 10px;
  }

  .library-item {
    padding: 8px;
  }

  .library-item .book-cover-container {
    width: 60px;
    height: 90px;
  }

  .library-item .book-title {
    font-size: 0.8rem;
  }

  .library-item .book-author {
    font-size: 0.7rem;
  }

  .action-buttons {
    justify-content: center;
  }

  .save-btn,
  .cancel-btn {
    padding: 8px 15px;
    font-size: 0.9rem;
  }
}
</style> 