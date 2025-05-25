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
  padding: 2rem;
  background: white;
  border-radius: 1rem;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
}

.section-title {
  font-size: 1.5rem;
  font-weight: bold;
  margin-bottom: 2rem;
  color: #333;
}

.top-books-section {
  margin-bottom: 2rem;
}

.description {
  color: #666;
  margin-bottom: 1rem;
}

.top-books-grid {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 1rem;
  margin-bottom: 2rem;
}

.rank-slot {
  background: #f8f9fa;
  border-radius: 0.5rem;
  padding: 1rem;
  min-height: 200px;
  position: relative;
}

.rank-number {
  position: absolute;
  top: 0.5rem;
  left: 0.5rem;
  background: rgb(0, 105, 0);
  color: white;
  padding: 0.25rem 0.5rem;
  border-radius: 0.25rem;
  font-size: 0.8rem;
}

.selected-book {
  display: flex;
  flex-direction: column;
  align-items: center;
  height: 100%;
}

.empty-slot {
  display: flex;
  align-items: center;
  justify-content: center;
  height: 100%;
  color: #888;
  font-size: 0.9rem;
}

.book-cover {
  width: 100%;
  max-width: 120px;
  aspect-ratio: 2/3;
  object-fit: cover;
  border-radius: 0.5rem;
  margin-bottom: 0.5rem;
}

.book-info {
  text-align: center;
}

.book-info h4 {
  font-size: 0.9rem;
  margin-bottom: 0.25rem;
  color: #333;
}

.book-info p {
  font-size: 0.8rem;
  color: #666;
}

.remove-btn {
  position: absolute;
  top: 0.5rem;
  right: 0.5rem;
  background: #dc3545;
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
}

.library-grid {
  display: grid;
  grid-template-columns: repeat(5, minmax(0, 1fr));
  gap: 1.5rem;
  margin-bottom: 2rem;
}

.library-item {
  background: white;
  border-radius: 0.5rem;
  padding: 1rem;
  transition: transform 0.2s;
  cursor: pointer;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
  display: flex;
  flex-direction: column;
  align-items: center;
  text-align: center;
  position: relative;
}

.library-item:hover {
  transform: translateY(-2px);
}

.library-item.selected {
  border: 2px solid rgb(0, 105, 0);
}

.library-item.selected::after {
  content: '✓';
  position: absolute;
  top: 0.5rem;
  right: 0.5rem;
  background: rgb(0, 105, 0);
  color: white;
  width: 24px;
  height: 24px;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 1rem;
}

.action-buttons {
  display: flex;
  justify-content: flex-end;
  gap: 1rem;
}

.save-btn, .cancel-btn {
  padding: 0.75rem 1.5rem;
  border-radius: 0.5rem;
  font-weight: bold;
  cursor: pointer;
  transition: background-color 0.2s;
}

.save-btn {
  background: rgb(0, 105, 0);
  color: white;
  border: none;
}

.save-btn:hover {
  background: rgb(0, 85, 0);
}

.cancel-btn {
  background: #f8f9fa;
  color: #666;
  border: 1px solid #ddd;
}

.cancel-btn:hover {
  background: #e9ecef;
}

@media (max-width: 1200px) {
  .library-grid {
    grid-template-columns: repeat(4, minmax(0, 1fr));
  }
}

@media (max-width: 992px) {
  .library-grid {
    grid-template-columns: repeat(3, minmax(0, 1fr));
  }
}

@media (max-width: 768px) {
  .library-grid {
    grid-template-columns: repeat(2, minmax(0, 1fr));
  }
  
  .top-books-grid {
    grid-template-columns: repeat(1, 1fr);
  }
}

@media (max-width: 480px) {
  .library-grid {
    grid-template-columns: repeat(1, minmax(0, 1fr));
  }
}
</style> 