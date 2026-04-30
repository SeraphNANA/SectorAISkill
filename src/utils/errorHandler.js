class AppError extends Error {
  constructor(message, code, details = {}) {
    super(message);
    this.name = 'AppError';
    this.code = code;
    this.details = details;
    this.timestamp = new Date().toISOString();
  }
}

class SpiderError extends AppError {
  constructor(message, details = {}) {
    super(message, 'SPIDER_ERROR', details);
    this.name = 'SpiderError';
  }
}

class FilterError extends AppError {
  constructor(message, details = {}) {
    super(message, 'FILTER_ERROR', details);
    this.name = 'FilterError';
  }
}

class ExtractError extends AppError {
  constructor(message, details = {}) {
    super(message, 'EXTRACT_ERROR', details);
    this.name = 'ExtractError';
  }
}

class RecommendError extends AppError {
  constructor(message, details = {}) {
    super(message, 'RECOMMEND_ERROR', details);
    this.name = 'RecommendError';
  }
}

function handleError(error, context = '') {
  const errorInfo = {
    timestamp: new Date().toISOString(),
    context,
    type: error.name || 'UnknownError',
    message: error.message,
    code: error.code || 'UNKNOWN',
    stack: error.stack
  };

  if (error instanceof AppError) {
    errorInfo.details = error.details;
  }

  console.error('❌ 错误发生:');
  console.error(`   上下文: ${context}`);
  console.error(`   类型: ${errorInfo.type}`);
  console.error(`   代码: ${errorInfo.code}`);
  console.error(`   消息: ${errorInfo.message}`);
  
  if (errorInfo.details && Object.keys(errorInfo.details).length > 0) {
    console.error(`   详情:`, errorInfo.details);
  }

  return errorInfo;
}

function wrapAsync(fn, context = '') {
  return async function(...args) {
    try {
      return await fn.apply(this, args);
    } catch (error) {
      handleError(error, context);
      throw error;
    }
  };
}

function safeExecute(fn, fallback = null, context = '') {
  try {
    return fn();
  } catch (error) {
    handleError(error, context);
    return fallback;
  }
}

async function safeExecuteAsync(fn, fallback = null, context = '') {
  try {
    return await fn();
  } catch (error) {
    handleError(error, context);
    return fallback;
  }
}

module.exports = {
  AppError,
  SpiderError,
  FilterError,
  ExtractError,
  RecommendError,
  handleError,
  wrapAsync,
  safeExecute,
  safeExecuteAsync
};
