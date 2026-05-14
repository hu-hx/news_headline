/**
 * API配置文件
 * 包含API基础URL和AI问答功能所需的API参数
 */

// API基础URL配置
export const apiConfig = {
  // 后端API基础URL
  baseURL: 'http://127.0.0.1:8000',
}

export const aiChatConfig = {
  // OpenAI API地址
  apiEndpoint: 'https://token-plan-cn.xiaomimimo.com/v1/chat/completions',
  
  // API Key (由开发人员指定)
  apiKey: 'tp-cwvl8sb0vadqpkj6and84niogbnxgk79vqjlfc1yagnn2suo',
  
  // 使用的模型
  model: 'mimo-v2-pro'
}
