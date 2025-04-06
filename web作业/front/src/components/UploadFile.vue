<template>
  <el-upload
    list-type="picture-card"
    :auto-upload="false"
    ref="uploadRef"
    :on-change="changeFile"
    method="post"
    :limit="1"
  >
    <el-icon><Plus /></el-icon>

    <template #file="{ file }">
      <div>
        <img class="el-upload-list__item-thumbnail" :src="file.url" alt="" />
        <span class="el-upload-list__item-actions">
          <span
            class="el-upload-list__item-preview"
            @click="handlePictureCardPreview(file)"
          >
            <el-icon><zoom-in /></el-icon>
          </span>
          <span
            v-if="!disabled"
            class="el-upload-list__item-delete"
            @click="handleDownload(file)"
          >
            <el-icon><Download /></el-icon>
          </span>
          <span
            v-if="!disabled"
            class="el-upload-list__item-delete"
            @click="handleRemove(file)"
          >
            <el-icon><Delete /></el-icon>
          </span>
        </span>
      </div>
    </template>
  </el-upload>

  <el-dialog v-model="dialogVisible">
    <img w-full :src="dialogImageUrl" alt="Preview Image" />
  </el-dialog>

  <el-button class="ml-3" type="success" @click="submitUpload">
    upload to server
  </el-button>
  <el-tag class="ml-3" >
    必须为 JPG 格式，且不超过 2MB
  </el-tag>
</template>
<script lang="ts" setup>
import { reactive, ref } from 'vue'
import { Delete, Download, Plus, ZoomIn } from '@element-plus/icons-vue'
import axios from 'axios'
import { ElMessage, UploadFile, UploadProps } from 'element-plus'
import type { UploadInstance } from 'element-plus'
const uploadRef = ref<UploadInstance>()
const dialogImageUrl = ref('')
const dialogVisible = ref(false)
const disabled = ref(false)
const file = ref()

const changeFile = (uploadFile: UploadFile) => {
  file.value = uploadFile
}

const handleRemove = (file: UploadFile) => {
  console.log(file)
}

const handlePictureCardPreview = (file: UploadFile) => {
  dialogImageUrl.value = file.url!
  dialogVisible.value = true
}

const handleDownload = (file: UploadFile) => {
  console.log(file)
}

const uploadForm = reactive({
  data: {
    fileId: '',
    name: '',
    type: ''
  }
})

const submitUpload = () => {
  const jsonStr = JSON.stringify(uploadForm.data)
  const blob = new Blob([jsonStr], {
    type: 'application/json'
  })
  let formData = new FormData()
  formData.append("obj", blob)
  // 这里很重要 file.value.raw才是真实的file文件，file.value只是一个Proxy代理对象
  formData.append("file", file.value.raw)
  let url = 'http://localhost:8081/file'
  if (file.value.raw.type !== 'image/jpeg') {
    ElMessage.error('图片必须是 JPG 格式!')
    return false
  } else if (file.value.raw.size / 1024 / 1024 > 2) {
    ElMessage.error('图片大小不超过 2MB!')
    return false
  }
  else
  {  axios({
    url,
    data: formData,
    method: 'post',
    headers: {
      'Content-Type': 'multipart/form-data'
    }
  }).then(res => {
    console.log(res)
    console.log(res.data)
  })}

}


</script>
