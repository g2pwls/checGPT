<template>
  <div class="ai-view">
    <div class="ai-content" ref="aiContent">
      <div class="container">
        <div v-if="book">
          <book-location :book="book"></book-location>
        </div>
        <div v-else class="no-book">
          <p>선택된 책이 없습니다.</p>
        </div>
      </div>
    </div>
    
    <div class="action-buttons">
      <button @click="saveAIReport" class="save-button">
        <i class="fas fa-save"></i> AI 레포트 저장하기
      </button>
    </div>
  </div>
</template>

<script>
import BookLocation from '@/components/BookLocation.vue'
import html2canvas from 'html2canvas'
import { jsPDF } from 'jspdf'
import axios from 'axios'

export default {
  name: 'AIView',
  components: {
    BookLocation
  },
  data() {
    return {
      book: null,
      loading: false,
      error: null
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
          this.$toast.success('AI 레포트가 저장되었습니다.')
        }
      } catch (error) {
        console.error('AI 레포트 저장 실패:', error)
        const errorMessage = error.response?.data?.detail || error.message || 'AI 레포트 저장에 실패했습니다.'
        this.$toast.error(errorMessage)
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
  padding: 30px 20px;
  background-color: #f5f7fa;
  min-height: 100vh;
}

.ai-content {
  background: white;
  border-radius: 16px;
  padding: 30px;
  margin-bottom: 20px;
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.05);
}

.container {
  max-width: 1200px;
  margin: 0 auto;
}

.no-book {
  text-align: center;
  padding: 50px;
  background-color: white;
  border-radius: 16px;
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.05);
}

.no-book p {
  color: #666;
  font-size: 1.1em;
}

.action-buttons {
  margin-top: 20px;
  text-align: center;
}

.save-button {
  background-color: #4CAF50;
  color: white;
  border: none;
  padding: 10px 20px;
  border-radius: 5px;
  cursor: pointer;
  font-size: 16px;
  display: flex;
  align-items: center;
  gap: 8px;
  margin: 0 auto;
}

.save-button:hover {
  background-color: #45a049;
}

.save-button i {
  font-size: 18px;
}
</style>