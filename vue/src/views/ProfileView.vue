<template>
  <div class="profile-container">
    <div class="content-wrapper">
      <!-- Left Sidebar -->
      <div class="left-sidebar">
        <div class="profile-box">
          <img 
            :src="getProfileImageUrl(user.profile_image)" 
            alt="프로필 사진" 
            class="profile-image"
            @error="handleImageError"
          />
          <h2 class="profile-name">{{ user.name }}</h2>
          <p class="profile-username">@{{ user.username }}</p>
          <div class="follow-stats">
            <div class="stat">
              <span class="stat-value">{{ user.followers_count || 0 }}</span>
              <span class="stat-label"> 팔로워</span>
            </div>
            <div class="stat">
              <span class="stat-value">{{ user.following_count || 0 }}</span>
              <span class="stat-label"> 팔로잉</span>
            </div>
          </div>
          <button 
            v-if="!isOwnProfile" 
            @click="toggleFollow" 
            :class="['follow-button', { 'following': user.is_following }]"
          >
            {{ user.is_following ? '팔로우 취소' : '+ 팔로우' }}
          </button>
        </div>
      </div>

      <!-- Right Content -->
      <div class="right-box">
        <div class="tabs">
          <button 
            @click="activeTab = 'library'" 
            :class="['tab-button', { active: activeTab === 'library' }]"
          >
            {{ user.name }}님의 서재
          </button>
          <button 
            @click="activeTab = 'threads'" 
            :class="['tab-button', { active: activeTab === 'threads' }]"
          >
            {{ user.name }}님의 스레드
          </button>
          <button 
            @click="activeTab = 'ai-reports'" 
            :class="['tab-button', { active: activeTab === 'ai-reports' }]"
          >
            AI 레포트
          </button>
        </div>

        <div class="tab-content">
          <!-- Library Tab -->
          <div v-if="activeTab === 'library'" class="library-content">
            <div v-if="isOwnProfile" class="library-actions">
              <button class="edit-btn" @click="openLibraryEdit">
                대표 도서 관리
              </button>
            </div>

            <!-- Top Books Section -->
            <div class="top-books-section">
              <h3 class="section-title section-title-normal">대표 도서</h3>
              <div v-if="topBooks.length > 0" class="top-books-grid">
                <div v-for="topBook in topBooks" :key="topBook.id" class="top-book-item" @click="goToBook(topBook.book.id)">
                  <div class="rank-badge">{{ topBook.rank }}순위</div>
                  <div class="book-cover-container">
                    <img :src="topBook.book.cover" :alt="topBook.book.title" class="book-cover">
                  </div>
                  <h3 class="book-title">{{ topBook.book.title }}</h3>
                  <p class="book-author">{{ topBook.book.author }}</p>
                </div>
              </div>
              <div v-else class="empty-state">
                <p>아직 대표 도서가 없습니다.</p>
              </div>
            </div>

            <!-- Top Genres Section -->
            <div v-if="topGenres.length > 0" class="top-genres-section">
              <h3 class="section-title section-title-normal">선호 장르</h3>
              <div class="top-genres-grid">
                <div v-for="(genre, index) in topGenres" :key="genre.id" class="genre-item">
                  <div class="rank-badge">{{ index + 1 }}순위</div>
                  <h4 class="genre-name">{{ genre.name }}</h4>
                  <p class="genre-count">{{ genre.count }}권</p>
                </div>
              </div>
            </div>

            <div v-if="library.length === 0" class="empty-state">
              <p>서재에 추가된 책이 없습니다.</p>
            </div>
            <div v-else class="library-grid">
              <div v-for="item in library" :key="item.id" class="library-item" @click="goToBook(item.book.id)">
                <div class="book-cover-container">
                  <img :src="item.book.cover" :alt="item.book.title" class="book-cover">
                </div>
                <h3 class="book-title">{{ item.book.title }}</h3>
                <p class="book-author">{{ item.book.author }}</p>
              </div>
            </div>
          </div>

          <!-- Threads Tab -->
          <div v-if="activeTab === 'threads'" class="threads-content">
            <div v-if="threads.length === 0" class="empty-state">
              <p>작성한 스레드가 없습니다.</p>
            </div>
            <div v-else class="threads-list">
              <div v-for="thread in threads" :key="thread.id" class="thread-item" @click="goToThread(thread.id)">
                <div class="thread-header">
                  <div class="book-info">
                    <img 
                      :src="thread.book.cover" 
                      :alt="thread.book.title" 
                      class="book-cover"
                      @error="handleImageError"
                    />
                    <span class="book-title">{{ thread.book.title }}</span>
                    <div class="book-details">
                      <div class="thread-meta">
                        <span class="author">by {{ thread.writer.username }}</span>
                        <span class="date">{{ formatDate(thread.read_date) }}</span>
                      </div>
                    </div>
                  </div>
                </div>
                <div class="thread-body">
                  <h3 class="thread-title">{{ thread.title }}</h3>
                  <p class="thread-content">{{ thread.content }}</p>
                </div>
                <div class="thread-footer">
                  <div class="interactions">
                    <span>❤️ {{ thread.likes_count }}</span>
                    <span>💬 {{ thread.comments_count }}</span>
                  </div>
                </div>
              </div>
            </div>
          </div>

          <!-- AI Reports Tab -->
          <div v-if="activeTab === 'ai-reports'" class="ai-reports-section">
            <h3>📊 AI 분석 레포트</h3>
            <div class="reports-grid">
              <div v-for="report in aiReports" :key="report.id" class="report-card">
                <div class="report-content" @click="showReport(report)">
                  <img :src="report.book.cover" :alt="report.book.title" class="book-cover">
                  <div class="report-info">
                    <h4>{{ report.book.title }}</h4>
                    <p class="report-date">{{ formatDate(report.created_at) }}</p>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- Library Edit Modal -->
    <div v-if="showLibraryEdit" class="modal-overlay">
      <div class="modal-content">
        <LibraryEdit 
          :library="library"
          @close="closeLibraryEdit"
          @update="updateLibrary"
        />
      </div>
    </div>

    <!-- AI Report Modal -->
    <div v-if="showReportModal" class="modal-overlay" @click="closeReportModal">
      <div class="modal-content" @click.stop>
        <button class="close-button" @click="closeReportModal">×</button>
        <h3>{{ selectedReport?.book.title }} AI 레포트</h3>
        <div class="report-viewer">
          <img 
            v-if="selectedReport?.report_image" 
            :src="getReportImageUrl(selectedReport.report_image)" 
            alt="AI Report" 
            class="report-image"
          />
          <div class="report-actions">
            <a 
              :href="getReportUrl(selectedReport?.report_file)" 
              target="_blank" 
              class="action-button download-btn"
            >
              <i class="fas fa-file-pdf"></i> PDF 다운로드
            </a>
            <button 
              v-if="isOwnProfile" 
              @click="deleteReport(selectedReport)" 
              class="action-button delete-btn"
            >
              <i class="fas fa-trash"></i> 레포트 삭제
            </button>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, computed, watch } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import axios from 'axios'
import LibraryEdit from '@/components/LibraryEdit.vue'

const route = useRoute()
const router = useRouter()
const user = ref({})
const threads = ref([])
const library = ref([])
const topBooks = ref([])
const topGenres = ref([])
const isFollowing = ref(false)
const activeTab = ref('library')
const showLibraryEdit = ref(false)
const aiReports = ref([])
const showReportModal = ref(false)
const selectedReport = ref(null)

// Check if this is the user's own profile
const isOwnProfile = computed(() => {
  const currentUserId = localStorage.getItem('userId')
  return !route.params.userId || route.params.userId === currentUserId
})

const getProfileImageUrl = (imagePath) => {
  if (!imagePath) return '/default-profile.png'
  if (imagePath.startsWith('http')) return imagePath
  return `http://127.0.0.1:8000${imagePath}`
}

const formatDate = (dateString) => {
  if (!dateString) return ''
  try {
    const date = new Date(dateString)
    if (isNaN(date.getTime())) return ''
    
    const year = date.getFullYear()
    const month = String(date.getMonth() + 1).padStart(2, '0')
    const day = String(date.getDate()).padStart(2, '0')
    
    return `${year}/${month}/${day}`
  } catch (error) {
    console.error('Date formatting error:', error)
    return ''
  }
}

const loadProfileData = async () => {
  try {
    const token = localStorage.getItem('token')
    if (!token) {
      router.push('/login')
      return
    }

    const userId = route.params.userId
    console.log('Current route userId:', userId)
    
    const endpoint = `http://127.0.0.1:8000/accounts/api/users/${userId}/profile/`
    
    console.log('Loading profile from:', endpoint)
    const res = await axios.get(endpoint, {
      headers: {
        Authorization: `Token ${token}`
      }
    })
    console.log('Profile response:', res.data)
    
    if (res.data) {
      user.value = res.data
      console.log('User value after setting:', user.value)
      isFollowing.value = user.value.is_following

      if (user.value.id) {
        console.log('User ID found:', user.value.id)
        try {
          // Load user's library
          const libraryEndpoint = `http://127.0.0.1:8000/api/users/${userId}/library/`
          console.log('Loading library from:', libraryEndpoint)
          
          try {
            const libraryRes = await axios.get(libraryEndpoint, {
              headers: {
                Authorization: `Token ${token}`
              }
            })
            console.log('Library response:', libraryRes)
            library.value = libraryRes.data.library
            topGenres.value = libraryRes.data.top_genres
          } catch (error) {
            console.error('Library loading error:', error)
            library.value = []
            topGenres.value = []
          }

          // Load user's threads
          try {
            const threadsEndpoint = `http://127.0.0.1:8000/api/users/${userId}/threads/`
            console.log('Loading threads from:', threadsEndpoint)
            const threadsRes = await axios.get(threadsEndpoint, {
              headers: {
                Authorization: `Token ${token}`
              }
            })
            console.log('Threads response:', threadsRes.data)
            threads.value = threadsRes.data
          } catch (error) {
            console.error('Error loading threads:', error)
            threads.value = []
          }

          // Load user's top books
          try {
            const topBooksEndpoint = `http://127.0.0.1:8000/api/users/${userId}/top-books/`
            console.log('Loading top books from:', topBooksEndpoint)
            const topBooksResponse = await axios.get(topBooksEndpoint, {
              headers: { Authorization: `Token ${token}` }
            })
            console.log('Top books response:', topBooksResponse.data)
            topBooks.value = topBooksResponse.data
          } catch (error) {
            console.error('Error loading top books:', error)
            topBooks.value = []
          }
        } catch (error) {
          console.error('Error loading user data:', error)
        }
      }
    } else {
      console.error('No user data received')
      user.value = {}
      threads.value = []
      library.value = []
      topBooks.value = []
      topGenres.value = []
    }
  } catch (error) {
    console.error("프로필 로딩 실패:", error)
    if (error.response) {
      if (error.response.status === 401) {
        router.push('/login')
      } else {
        user.value = {}
        threads.value = []
        library.value = []
        topBooks.value = []
        topGenres.value = []
      }
    }
  }
}

const handleImageError = (e) => {
  console.log('Image load error, using default image')
  e.target.src = '/default-profile.png'
}

const toggleFollow = async () => {
  try {
    const token = localStorage.getItem('token')
    if (!token) {
      alert('로그인이 필요합니다.')
      return
    }

    const currentUserId = localStorage.getItem('userId')
    if (currentUserId === route.params.userId) {
      alert('자기 자신을 팔로우할 수 없습니다.')
      return
    }

    const newFollowStatus = !user.value.is_following
    user.value.is_following = newFollowStatus
    user.value.followers_count += newFollowStatus ? 1 : -1

    const response = await axios.post(
      `http://127.0.0.1:8000/accounts/api/follow/${route.params.userId}/`,
      {},
      {
        headers: {
          Authorization: `Token ${token}`
        }
      }
    )
    
    const profileRes = await axios.get(
      `http://127.0.0.1:8000/accounts/api/users/${route.params.userId}/profile/`,
      {
        headers: {
          Authorization: `Token ${token}`
        }
      }
    )
    
    user.value = profileRes.data
    user.value = { ...user.value }
  } catch (error) {
    console.error("팔로우 토글 실패:", error)
    user.value.is_following = !user.value.is_following
    user.value.followers_count += user.value.is_following ? 1 : -1
    user.value = { ...user.value }

    if (error.response) {
      if (error.response.status === 400) {
        alert(error.response.data.error || '팔로우할 수 없습니다.')
      } else if (error.response.status === 401) {
        alert('로그인이 필요합니다.')
      }
    }
  }
}

const goToThread = (threadId) => {
  router.push(`/threads/${threadId}`)
}

const goToBook = (bookId) => {
  router.push(`/books/${bookId}`)
}

const openLibraryEdit = () => {
  showLibraryEdit.value = true
}

const closeLibraryEdit = () => {
  showLibraryEdit.value = false
}

const updateLibrary = () => {
  loadProfileData()
}

const fetchAIReports = async () => {
  try {
    const response = await axios.get('http://127.0.0.1:8000/api/ai-reports/', {
      headers: {
        Authorization: `Token ${localStorage.getItem('token')}`
      }
    })
    aiReports.value = response.data
  } catch (error) {
    console.error('AI 레포트 로딩 실패:', error)
  }
}

const showReport = (report) => {
  selectedReport.value = report
  showReportModal.value = true
}

const closeReportModal = () => {
  showReportModal.value = false
  selectedReport.value = null
}

const getReportUrl = (reportFile) => {
  if (!reportFile) return ''
  if (reportFile.startsWith('http')) return reportFile
  return `http://127.0.0.1:8000${reportFile}`
}

const deleteReport = async (report) => {
  if (!confirm('정말로 이 AI 레포트를 삭제하시겠습니까?')) {
    return
  }

  try {
    await axios.delete(`http://127.0.0.1:8000/api/ai-reports/${report.id}/`, {
      headers: {
        Authorization: `Token ${localStorage.getItem('token')}`
      }
    })
    
    // 삭제 후 목록 새로고침
    aiReports.value = aiReports.value.filter(r => r.id !== report.id)
    // 모달창 닫기
    closeReportModal()
  } catch (error) {
    console.error('AI 레포트 삭제 실패:', error)
    alert('레포트 삭제에 실패했습니다. 다시 시도해주세요.')
  }
}

const getReportImageUrl = (imagePath) => {
  if (!imagePath) return ''
  if (imagePath.startsWith('http')) return imagePath
  return `http://127.0.0.1:8000${imagePath}`
}

onMounted(() => {
  loadProfileData()
  fetchAIReports()
})

watch(
  () => route.params.userId,
  (newUserId, oldUserId) => {
    if (newUserId !== oldUserId) {
      loadProfileData()
    }
  },
  { immediate: true }
)
</script>

<style scoped>
.profile-container {
  background-color: #ffffff; /* 밝은 회색 배경 */
  font-family: 'Noto Sans KR', sans-serif;
  color: #333; /* 어두운 글자색 */
  min-height: 100vh; /* 최소 높이 설정 */
  padding: 20px;
}

.content-wrapper {
  max-width: 1200px;
  margin: 0 auto;
  display: flex;
  gap: 20px;
}

.left-sidebar {
  width: 280px; /* 고정 너비 */
  flex-shrink: 0;
}

.profile-box {
  background-color: #ffffff; /* 흰색 배경 */
  padding: 20px;
  border-radius: 8px;
  box-shadow: 0 2px 5px rgba(0, 0, 0, 0.05);
  text-align: center;
  border: 1px solid #ddd;
}

.profile-image {
  width: 120px;
  height: 120px;
  border-radius: 50%;
  object-fit: cover;
  margin-bottom: 5px;
  border: 1px solid #ddd; /* 테두리 추가 */
}

.profile-name {
  font-size: 1.8rem;
  font-weight: bold;
  margin-bottom: 5px;
  color: #333;
}

.profile-username {
  font-size: 1rem;
  color: #777;
  margin-bottom: 20px;
}

.follow-stats {
  display: flex;
  justify-content: center;
  gap: 20px;
  margin-bottom: 20px;
}

.stat {
  text-align: center;
}

.stat-value {
  font-size: 1.2rem;
  font-weight: bold;
  color: #333;
}

.stat-label {
  font-size: 0.9rem;
  color: #777;
}

.follow-button {
  padding: 10px 20px;
  border: none;
  border-radius: 4px;
  cursor: pointer;
  font-size: 1rem;
  transition: background-color 0.2s ease;
  width: 100%;
}

.follow-button:not(.following) {
  background-color: #007bff; /* 파란색 계열 (예시) */
  color: white;
}

.follow-button:not(.following):hover {
  background-color: #0056b3;
}

.follow-button.following {
  background-color: #dc3545; /* 빨간색 계열 (예시) */
  color: white;
}

.follow-button.following:hover {
  background-color: #c82333;
}

.right-box {
  flex: 1;
  background-color: #ffffff; /* 흰색 배경 */
  padding: 20px;
  border-radius: 0px;
  box-shadow: 0 2px 5px rgba(0, 0, 0, 0.05);
  border: 1px solid #ddd;
}

.tabs {
  display: flex;
  border-bottom: 1px solid #ddd;
  margin-bottom: 20px;
}

.tab-button {
  padding: 10px 15px;
  border: none;
  background: none;
  cursor: pointer;
  font-size: 1rem;
  color: #777;
  transition: color 0.2s ease, border-bottom-color 0.2s ease;
  border-bottom: 2px solid transparent;
}

.tab-button:hover {
  color: #333;
}

.tab-button.active {
  color: #333;
  font-weight: bold;
  border-bottom-color: #333;
}

.library-actions {
  margin-bottom: 20px;
  text-align: right;
}

.edit-btn {
  padding: 8px 15px;
  border: 1px solid #ddd;
  border-radius: 4px;
  background-color: #eee;
  cursor: pointer;
  font-size: 0.9rem;
}

.edit-btn:hover {
  background-color: #ddd;
}

.section-title {
  font-size: 1.5rem;
  font-weight: bold;
  margin-bottom: 15px;
  color: #333;
  border-bottom: 1px solid #eee;
  padding-bottom: 10px;
}

.section-title.section-title-normal {
  font-weight: 400;
}

.top-books-grid,
.library-grid,
.top-genres-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(150px, 1fr));
  gap: 20px;
}

.top-book-item,
.library-item {
  background-color: #f9f9f9; /* 밝은 배경 */
  padding: 15px;
  border-radius: 8px;
  text-align: center;
  border: 1px solid #eee;
  box-shadow: 0 1px 3px rgba(0, 0, 0, 0.03);
  transition: all 0.2s ease;
  cursor: pointer;
}

.top-book-item:hover,
.library-item:hover {
  transform: translateY(-2px);
  box-shadow: 0 3px 6px rgba(0, 0, 0, 0.06);
}

.rank-badge {
  display: inline-block;
  background-color: #333; /* 무채색 배지 */
  color: white;
  font-size: 0.8rem;
  padding: 3px 8px;
  border-radius: 12px;
  margin-bottom: 10px;
}

.book-cover-container {
  width: 100px;
  height: 150px;
  margin: 0 auto 10px;
}

.book-cover {
  width: 100%;
  height: 100%;
  object-fit: cover;
  border-radius: 4px;
  border: 1px solid #ddd;
}

.book-title {
  font-size: 1rem;
  font-weight: bold;
  margin-bottom: 4px;
  color: #333;
}

.book-author {
  font-size: 0.9rem;
  color: #777;
}

.genre-item {
  background-color: #f9f9f9; /* 밝은 배경 */
  padding: 15px;
  border-radius: 8px;
  text-align: center;
  border: 1px solid #eee;
  box-shadow: 0 1px 3px rgba(0, 0, 0, 0.03);
}

.genre-name {
  font-size: 1.1rem;
  font-weight: bold;
  margin-bottom: 5px;
  color: #333;
}

.genre-count {
  font-size: 0.9rem;
  color: #777;
}

.empty-state {
  text-align: center;
  color: #777;
  padding: 50px 0;
}

.threads-list {
  display: flex;
  flex-direction: column;
  gap: 15px;
}

.thread-item {
  background-color: #f9f9f9; /* 밝은 배경 */
  padding: 15px;
  border-radius: 8px;
  border: 1px solid #eee;
  box-shadow: 0 1px 3px rgba(0, 0, 0, 0.03);
  transition: all 0.2s ease;
  cursor: pointer;
}

.thread-item:hover {
  transform: translateY(-2px);
  box-shadow: 0 3px 6px rgba(0, 0, 0, 0.06);
}

.thread-header {
  display: flex;
  align-items: center;
  gap: 15px;
  margin-bottom: 10px;
}

.thread-header .book-info {
  display: flex;
  align-items: center;
  gap: 10px;
}

.thread-header .book-cover {
  width: 50px;
  height: 75px;
  object-fit: cover;
  border-radius: 4px;
  border: 1px solid #ddd;
}

.thread-header .book-title {
  font-size: 1rem;
  font-weight: bold;
  color: #333;
}

.thread-meta {
  font-size: 0.85rem;
  color: #777;
}

.thread-meta .author {
  font-weight: bold;
  margin-right: 10px;
}

.thread-body h3 {
  font-size: 1.2rem;
  font-weight: bold;
  margin-bottom: 10px;
  color: #333;
}

.thread-body .thread-content {
  font-size: 1rem;
  color: #555;
  line-height: 1.5;
  margin-bottom: 10px;
}

.thread-footer .interactions span {
  font-size: 0.9rem;
  color: #777;
  margin-right: 15px;
}

.ai-reports-section h3 {
  font-size: 1.5rem;
  font-weight: bold;
  margin-bottom: 15px;
  color: #333;
  border-bottom: 1px solid #eee;
  padding-bottom: 10px;
}

.reports-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(150px, 1fr));
  gap: 20px;
}

.report-card {
  background-color: #f9f9f9; /* 밝은 배경 */
  padding: 15px;
  border-radius: 8px;
  border: 1px solid #eee;
  box-shadow: 0 1px 3px rgba(0, 0, 0, 0.03);
  transition: all 0.2s ease;
  cursor: pointer;
}

.report-card:hover {
  transform: translateY(-2px);
  box-shadow: 0 3px 6px rgba(0, 0, 0, 0.06);
}

.report-content {
  display: flex;
  flex-direction: column;
  align-items: center;
  text-align: center;
  gap: 10px;
}

.report-card .book-cover {
  width: 80px;
  height: 120px;
  object-fit: cover;
  border-radius: 4px;
  border: 1px solid #ddd;
}

.report-info h4 {
  font-size: 1rem;
  font-weight: bold;
  margin-bottom: 5px;
  color: #333;
}

.report-date {
  font-size: 0.85rem;
  color: #777;
}

.modal-overlay {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background-color: rgba(0, 0, 0, 0.5); /* 어두운 오버레이 */
  display: flex;
  justify-content: center;
  align-items: center;
  z-index: 1000;
}

.modal-content {
  background-color: #ffffff; /* 흰색 배경 */
  padding: 30px;
  border-radius: 8px;
  box-shadow: 0 4px 15px rgba(0, 0, 0, 0.2);
  max-width: 800px;
  width: 90%;
  position: relative;
}

.close-button {
  position: absolute;
  top: 10px;
  right: 10px;
  font-size: 1.5rem;
  border: none;
  background: none;
  cursor: pointer;
  color: #777;
}

.close-button:hover {
  color: #333;
}

.report-viewer {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 20px;
  margin-top: 20px;
}

.report-image {
  max-width: 100%;
  height: auto;
  border: 1px solid #ddd;
  border-radius: 4px;
}

.report-actions {
  display: flex;
  gap: 15px;
}

.action-button {
  padding: 10px 20px;
  border: none;
  border-radius: 4px;
  cursor: pointer;
  font-size: 1rem;
  display: flex;
  align-items: center;
  gap: 8px;
  transition: background-color 0.2s ease;
}

.download-btn {
  background-color: #333; /* 무채색 다운로드 버튼 */
  color: white;
}

.download-btn:hover {
  background-color: #555;
}

.delete-btn {
  background-color: #dc3545; /* 빨간색 삭제 버튼 */
  color: white;
}

.delete-btn:hover {
  background-color: #c82333;
}

/* AI 레포트 관련 버튼 (ProfileView에 AI 분석 시작하기 버튼이 없으므로 AI 레포트 모달 내 버튼에 적용) */
/* ProfileView에는 AI 분석 시작하기 버튼이 없으므로, AI 관련 기능 버튼은 AI Report Modal 내의 버튼에 적용 */
/* AI 레포트 다운로드 버튼은 AI 관련 기능으로 간주하여 빨간색 적용 */
.report-viewer .action-button.download-btn {
    background-color: #e74c3c; /* 요청된 빨간색 */
    color: white;
}

.report-viewer .action-button.download-btn:hover {
    background-color: #ff7676; /* 기존 빨간색보다 밝게 */
}

@media (max-width: 768px) {
  .content-wrapper {
    flex-direction: column;
  }

  .left-sidebar {
    width: 100%;
    text-align: center;
  }

  .profile-image {
    width: 100px;
    height: 100px;
  }

  .follow-stats {
    justify-content: center;
  }

  .right-box {
    padding: 15px;
  }

  .tabs {
    flex-wrap: wrap;
    justify-content: center;
    gap: 10px;
    border-bottom: none;
  }

  .tab-button {
    border-bottom: none;
  }

  .tab-button.active {
    border-bottom: 2px solid #333;
  }

  .top-books-grid,
  .library-grid,
  .top-genres-grid,
  .reports-grid {
    grid-template-columns: repeat(auto-fill, minmax(120px, 1fr));
    gap: 15px;
  }

  .top-book-item,
  .library-item,
  .genre-item,
  .report-card {
    padding: 10px;
  }

  .book-cover-container {
    width: 80px;
    height: 120px;
  }

  .thread-header {
    flex-direction: column;
    align-items: flex-start;
  }

  .thread-header .book-info {
    flex-direction: column;
    align-items: flex-start;
  }

  .modal-content {
    padding: 20px;
  }

  .report-actions {
    flex-direction: column;
    gap: 10px;
  }
}
</style>
