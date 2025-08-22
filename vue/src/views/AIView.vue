<template>
  <div class="ai-view">
    <div v-if="loading" class="ai-loading-overlay">
      <div class="ai-spinner"></div>
    </div>
    <div class="ai-content" ref="aiContent">
      <div class="container">
        <div v-if="book">
          <div class="ai-card">
            <book-location :book="book"></book-location>
            <AIMusic :book="book" />
            <AIMovie :book="book" />
          </div>
        </div>
        <div v-else class="no-book">
          <p>선택된 책이 없습니다.</p>
        </div>
      </div>
    </div>
    <div class="action-buttons">
      <button @click="saveAIReport" class="save-button" :disabled="loading">
        <i class="fas fa-save"></i> 
        {{ buttonText }}
      </button>
    </div>
  </div>
</template>

<script>
import AIMusic from '@/components/AIMusic.vue'
import AIMovie from '@/components/AIMovie.vue'
import BookLocation from '@/components/BookLocation.vue'
import html2canvas from 'html2canvas'
import { jsPDF } from 'jspdf'
import axios from 'axios'

export default {
  name: 'AIView',
  components: {
    BookLocation,
    AIMusic,
    AIMovie
  },
  data() {
    return {
      book: null,
      loading: false,
      error: null,
      isCompleted: false
    }
  },
  computed: {
    buttonText() {
      if (this.loading) {
        return '저장 중...'
      }
      if (this.isCompleted) {
        return 'AI 레포트 저장 완료'
      }
      return 'AI 레포트 저장하기'
    }
  },
  created() {
    // 라우터 파라미터에서 책 정보 가져오기
    const bookData = this.$route.params.book
    if (bookData) {
      this.book = typeof bookData === 'string' ? JSON.parse(bookData) : bookData
    }
  },
  methods: {
    async saveAIReport() {
      this.loading = true
      this.error = null
      this.isCompleted = false
      
      try {
        // AI 분석 내용을 이미지로 변환
        const element = this.$refs.aiContent
        if (!element) {
          throw new Error('AI 분석 내용을 찾을 수 없습니다.')
        }

        // html2canvas 옵션 설정
        const canvas = await html2canvas(element, {
          useCORS: true,
          scale: 2,
          logging: false,
          allowTaint: true,
          backgroundColor: '#ffffff'
        })
        
        // 이미지 데이터 생성
        const imgData = canvas.toDataURL('image/png')
        
        // 이미지 Blob 생성
        const imgBlob = await (await fetch(imgData)).blob()
        
        // PDF 생성
        const pdf = new jsPDF({
          orientation: 'portrait',
          unit: 'mm'
        })
        
        const pdfWidth = pdf.internal.pageSize.getWidth()
        const pdfHeight = (canvas.height * pdfWidth) / canvas.width
        pdf.addImage(imgData, 'PNG', 0, 0, pdfWidth, pdfHeight)
        
        // PDF를 Blob으로 변환
        const pdfBlob = pdf.output('blob')
        
        // FormData 생성
        const formData = new FormData()
        formData.append('report_file', pdfBlob, 'ai_report.pdf')
        formData.append('report_image', imgBlob, 'ai_report.png')
        formData.append('book', this.book.id.toString())
        
        // 서버에 저장
        const response = await axios.post('http://127.0.0.1:8000/api/ai-reports/', formData, {
          headers: {
            'Content-Type': 'multipart/form-data',
            'Authorization': `Token ${localStorage.getItem('token')}`
          }
        })
        
        if (response.data) {
          this.$toast.success('AI 레포트가 저장되었습니다.', {
            position: 'top-right',
            duration: 3000
          })
          this.isCompleted = true
        }
      } catch (error) {
        console.error('AI 레포트 저장 실패:', error)
        const errorMessage = error.response?.data?.detail || error.message || 'AI 레포트 저장에 실패했습니다.'
        this.$toast.error(errorMessage, {
          position: 'top-right',
          duration: 3000
        })
        this.error = errorMessage
      } finally {
        this.loading = false
      }
    }
  }
}

</script>

<style scoped>
.ai-view {
  padding: 20px;
  min-height: 100vh;
  background-color: #ffffff;
}

.container {
  max-width: 1200px;
  margin: 0 auto;
}

.ai-card {
  background: white;
  border-radius: 0px;
  box-shadow: 0 2px 5px rgba(0, 0, 0, 0.5);
  overflow: hidden;
  border: 1px solid #eee;
  padding: 20px;
  display: flex;
  flex-direction: column;
  gap: 20px;
}

.ai-card > * {
  width: 100%;
}

.no-book {
  text-align: center;
  padding: 40px;
  background: white;
  border-radius: 10px;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
}

.action-buttons {
  position: fixed;
  bottom: 20px;
  right: 20px;
  z-index: 1000;
}

.save-button {
  background-color: #e53935;
  color: white;
  border: none;
  padding: 12px 24px;
  border-radius: 5px;
  cursor: pointer;
  font-size: 1rem;
  display: flex;
  align-items: center;
  gap: 8px;
  transition: background-color 0.3s;
}

.save-button:hover {
  background-color: #e74c3c;
}

.save-button:disabled {
  background-color: #cccccc;
  cursor: not-allowed;
}

.save-button i {
  font-size: 1.2rem;
}

@media (max-width: 768px) {
  .save-button {
    width: 100%;
    justify-content: center;
  }
}

.ai-loading-overlay {
  position: fixed;
  top: 0; left: 0; right: 0; bottom: 0;
  background: rgba(255,255,255,0.7);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 2000;
}
.ai-spinner {
  width: 48px;
  height: 48px;
  border: 6px solid #e0e0e0;
  border-top: 6px solid #222;
  border-radius: 50%;
  animation: ai-spin 1s linear infinite;
  background: transparent;
}
@keyframes ai-spin {
  0% { transform: rotate(0deg);}
  100% { transform: rotate(360deg);}
}
</style>