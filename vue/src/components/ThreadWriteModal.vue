<template>
    <div class="modal-overlay">
      <div class="form-box">
        <h2 class="title">{{book.title}} 스레드 작성</h2>
  
        <label class="label">제목</label>
        <input v-model="title" type="text" placeholder="제목 입력" class="input" />
  
        <label class="label">내용</label>
        <textarea v-model="content" placeholder="내용 입력" class="textarea" />
  
        <label class="label">읽은 날짜</label>
        <input v-model="readDate" type="date" class="input" />
  
        <div class="button-group">
          <button class="cancel" @click="$emit('close')">취소</button>
          <button class="submit" @click="submitThread">작성</button>
        </div>
      </div>
    </div>
  </template>
  
  <script>
import axios from 'axios'

export default {
  props: ['book'],
  data() {
    return {
      title: '',
      content: '',
      readDate: ''
    }
  },
  methods: {
    async submitThread() {
      const thread = {
        title: this.title,
        content: this.content,
        read_date: this.readDate,   // readDate → read_date로 변경 (Django 필드 이름에 맞게)
        author: this.book.author,             // 고정 값, 또는 로그인 유저에서 가져오도록 추후 개선
        book: this.book.id          // bookId → book (Django 필드 이름에 맞게)
      }

      try {
        const response = await axios.post('http://localhost:8000/api/threads/', thread)
        alert('작성 완료!')
        this.$emit('submit-thread', response.data)  // 필요시 부모에게 전파
        this.$emit('close')
      } catch (error) {
        console.error('스레드 저장 실패:', error)
        alert('작성 중 오류가 발생했습니다.')
      }
    }
  }
}
</script>

  
  <style scoped>
  .modal-overlay {
    position: fixed;
    top: 0;
    left: 0;
    width: 100%;
    height: 100%;
    background: rgba(0,0,0,0.6);
    display: flex;
    align-items: center;
    justify-content: center;
    z-index: 999;
  }
  
  .form-box {
    background-color: #fff;
    color: black;
    border-radius: 10px;
    padding: 40px;
    width: 600px;
    max-width: 90%;
  }
  
  .title {
    text-align: center;
    font-size: 24px;
    font-weight: bold;
    margin-bottom: 30px;
  }
  
  .label {
    display: block;
    margin-top: 20px;
    font-weight: bold;
    font-size: 14px;
  }
  
  .input,
  .textarea {
    width: 95%;
    padding: 12px;
    margin-top: 6px;
    border: 1px solid #ccc;
    border-radius: 6px;
    font-size: 14px;
    background-color: #f9f9f9;
  }
  
  .textarea {
    height: 150px;
    resize: none;
  }
  
  .button-group {
    display: flex;
    justify-content: space-between;
    margin-top: 30px;
  }
  
  .cancel,
  .submit {
    width: 48%;
    padding: 12px;
    font-size: 16px;
    border: none;
    border-radius: 6px;
    cursor: pointer;
  }
  
  .cancel {
    background-color: #fff;
    color: #f44;
    border: 1px solid #f44;
  }
  
  .submit {
    background-color: #f44;
    color: white;
  }
  </style>
  