import { useState } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import { Upload, FileText, Sparkles, CheckCircle, XCircle, TrendingUp, Award } from 'lucide-react';
import axios from 'axios';
import './App.css';

function App() {
  const [file, setFile] = useState(null);
  const [jobDescription, setJobDescription] = useState('');
  const [result, setResult] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');
  const [dragActive, setDragActive] = useState(false);

  const handleFileChange = (e) => {
    const selectedFile = e.target.files[0];
    if (selectedFile) {
      setFile(selectedFile);
      setError('');
    }
  };

  const handleDrag = (e) => {
    e.preventDefault();
    e.stopPropagation();
    if (e.type === 'dragenter' || e.type === 'dragover') {
      setDragActive(true);
    } else if (e.type === 'dragleave') {
      setDragActive(false);
    }
  };

  const handleDrop = (e) => {
    e.preventDefault();
    e.stopPropagation();
    setDragActive(false);

    if (e.dataTransfer.files && e.dataTransfer.files[0]) {
      setFile(e.dataTransfer.files[0]);
      setError('');
    }
  };

  const handleSubmit = async () => {
    if (!file) {
      setError('Please select a resume file');
      return;
    }

    setLoading(true);
    setError('');
    setResult(null);

    const formData = new FormData();
    formData.append('resume', file);
    formData.append('job_description', jobDescription);

    try {
      const response = await axios.post('http://localhost:5000/analyze', formData, {
        headers: {
          'Content-Type': 'multipart/form-data',
        },
      });

      setResult(response.data);
    } catch (err) {
      setError(err.response?.data?.error || 'Failed to analyze resume. Please try again.');
    } finally {
      setLoading(false);
    }
  };

  const getScoreColor = (score) => {
    if (score >= 80) return 'text-green-400';
    if (score >= 60) return 'text-yellow-400';
    return 'text-red-400';
  };

  const getCircleProgress = (score) => {
    const circumference = 2 * Math.PI * 70;
    return circumference - (score / 100) * circumference;
  };

  return (
    <div className="min-h-screen bg-gradient-to-br from-gray-900 via-purple-900 to-violet-900 animate-gradient">
      <div className="absolute inset-0 overflow-hidden pointer-events-none">
        <div className="absolute top-20 left-20 w-72 h-72 bg-purple-500 rounded-full mix-blend-multiply filter blur-xl opacity-20 animate-float"></div>
        <div className="absolute top-40 right-20 w-72 h-72 bg-pink-500 rounded-full mix-blend-multiply filter blur-xl opacity-20 animate-float" style={{ animationDelay: '2s' }}></div>
        <div className="absolute bottom-20 left-1/2 w-72 h-72 bg-indigo-500 rounded-full mix-blend-multiply filter blur-xl opacity-20 animate-float" style={{ animationDelay: '4s' }}></div>
      </div>

      <div className="relative z-10 container mx-auto px-4 py-12">
        <motion.div
          initial={{ opacity: 0, y: -50 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.8 }}
          className="text-center mb-12"
        >
          <div className="flex items-center justify-center mb-4">
            <Sparkles className="w-12 h-12 text-yellow-400 mr-3 animate-pulse" />
            <h1 className="text-6xl font-bold text-white">
              AI Resume <span className="text-transparent bg-clip-text bg-gradient-to-r from-purple-400 to-pink-600">Analyzer</span>
            </h1>
          </div>
          <p className="text-gray-300 text-xl">Upload your resume and get instant AI-powered feedback</p>
        </motion.div>

        <div className="max-w-6xl mx-auto">
          <div className="grid grid-cols-1 lg:grid-cols-2 gap-8">

            <motion.div
              initial={{ opacity: 0, x: -50 }}
              animate={{ opacity: 1, x: 0 }}
              transition={{ duration: 0.8, delay: 0.2 }}
            >
              <div className="glass rounded-3xl p-8 shadow-2xl">
                <h2 className="text-2xl font-bold text-white mb-6 flex items-center">
                  <Upload className="mr-2" /> Upload Resume
                </h2>

                <div
                  className={`border-3 border-dashed rounded-2xl p-12 text-center transition-all ${dragActive ? 'border-purple-400 bg-purple-900/30' : 'border-gray-600 hover:border-purple-500'
                    }`}
                  onDragEnter={handleDrag}
                  onDragLeave={handleDrag}
                  onDragOver={handleDrag}
                  onDrop={handleDrop}
                >
                  <input
                    type="file"
                    accept=".pdf,.docx,.txt"
                    onChange={handleFileChange}
                    className="hidden"
                    id="fileInput"
                  />
                  <label htmlFor="fileInput" className="cursor-pointer flex flex-col items-center">
                    <FileText className="w-20 h-20 text-purple-400 mb-4" />
                    <p className="text-white text-lg font-semibold mb-2">
                      {file ? file.name : 'Drop your resume here or click to browse'}
                    </p>
                    <p className="text-gray-400 text-sm">Supports PDF, DOCX, TXT (Max 16MB)</p>
                  </label>
                </div>

                <div className="mt-6">
                  <label className="text-white font-semibold mb-2 block">Job Description (Optional)</label>
                  <textarea
                    value={jobDescription}
                    onChange={(e) => setJobDescription(e.target.value)}
                    placeholder="Paste the job description here for better matching..."
                    className="w-full bg-gray-800/50 text-white rounded-xl p-4 h-32 resize-none focus:outline-none focus:ring-2 focus:ring-purple-500"
                  />
                </div>

                <motion.button
                  whileHover={{ scale: 1.05 }}
                  whileTap={{ scale: 0.95 }}
                  onClick={handleSubmit}
                  disabled={loading}
                  className="w-full mt-6 bg-gradient-to-r from-purple-600 to-pink-600 text-white font-bold py-4 rounded-xl shadow-lg hover:shadow-purple-500/50 disabled:opacity-50 disabled:cursor-not-allowed flex items-center justify-center"
                >
                  {loading ? (
                    <>
                      <div className="animate-spin rounded-full h-5 w-5 border-b-2 border-white mr-2"></div>
                      Analyzing...
                    </>
                  ) : (
                    <>
                      <Sparkles className="mr-2" /> Analyze Resume
                    </>
                  )}
                </motion.button>

                {error && (
                  <motion.div
                    initial={{ opacity: 0 }}
                    animate={{ opacity: 1 }}
                    className="mt-4 bg-red-500/20 border border-red-500 text-red-200 p-4 rounded-xl"
                  >
                    {error}
                  </motion.div>
                )}
              </div>
            </motion.div>

            <motion.div
              initial={{ opacity: 0, x: 50 }}
              animate={{ opacity: 1, x: 0 }}
              transition={{ duration: 0.8, delay: 0.4 }}
            >
              <AnimatePresence mode="wait">
                {result ? (
                  <motion.div
                    key="results"
                    initial={{ opacity: 0, scale: 0.9 }}
                    animate={{ opacity: 1, scale: 1 }}
                    exit={{ opacity: 0, scale: 0.9 }}
                    className="glass rounded-3xl p-8 shadow-2xl"
                  >
                    <h2 className="text-2xl font-bold text-white mb-6 flex items-center">
                      <Award className="mr-2 text-yellow-400" /> Analysis Results
                    </h2>

                    <div className="flex justify-center mb-8">
                      <div className="relative">
                        <svg className="transform -rotate-90 w-48 h-48">
                          <circle cx="96" cy="96" r="70" stroke="currentColor" strokeWidth="12" fill="transparent" className="text-gray-700" />
                          <motion.circle
                            cx="96"
                            cy="96"
                            r="70"
                            stroke="currentColor"
                            strokeWidth="12"
                            fill="transparent"
                            strokeDasharray={2 * Math.PI * 70}
                            strokeDashoffset={getCircleProgress(result.score.overall_score)}
                            className={getScoreColor(result.score.overall_score)}
                            initial={{ strokeDashoffset: 2 * Math.PI * 70 }}
                            animate={{ strokeDashoffset: getCircleProgress(result.score.overall_score) }}
                            transition={{ duration: 1.5, ease: 'easeOut' }}
                          />
                        </svg>
                        <div className="absolute inset-0 flex items-center justify-center flex-col">
                          <span className={`text-5xl font-bold ${getScoreColor(result.score.overall_score)}`}>
                            {result.score.overall_score}
                          </span>
                          <span className="text-gray-400 text-sm">out of 100</span>
                        </div>
                      </div>
                    </div>

                    <div className="space-y-4 mb-6">
                      {[
                        { name: 'Section Completeness', score: result.score.section_score, max: 30 },
                        { name: 'Length Optimization', score: result.score.length_score, max: 20 },
                        { name: 'Keyword Density', score: result.score.keyword_score, max: 20 },
                        { name: 'Formatting Quality', score: result.score.formatting_score, max: 15 },
                        { name: 'JD Match', score: result.score.jd_match_score, max: 15 },
                      ].map((item, index) => (
                        <motion.div
                          key={index}
                          initial={{ opacity: 0, x: -20 }}
                          animate={{ opacity: 1, x: 0 }}
                          transition={{ delay: 0.1 * index }}
                        >
                          <div className="flex justify-between text-sm mb-1">
                            <span className="text-gray-300">{item.name}</span>
                            <span className="text-white font-semibold">{item.score}/{item.max}</span>
                          </div>
                          <div className="w-full bg-gray-700 rounded-full h-2">
                            <motion.div
                              className="bg-gradient-to-r from-purple-500 to-pink-500 h-2 rounded-full"
                              initial={{ width: 0 }}
                              animate={{ width: `${(item.score / item.max) * 100}%` }}
                              transition={{ duration: 1, delay: 0.1 * index }}
                            />
                          </div>
                        </motion.div>
                      ))}
                    </div>

                    <div className="mb-6">
                      <h3 className="text-lg font-semibold text-white mb-3">Detected Sections</h3>
                      <div className="grid grid-cols-2 gap-2">
                        {Object.entries(result.sections).map(([key, value]) => (
                          <div key={key} className="flex items-center text-sm">
                            {value ? (
                              <CheckCircle className="w-4 h-4 text-green-400 mr-2" />
                            ) : (
                              <XCircle className="w-4 h-4 text-red-400 mr-2" />
                            )}
                            <span className={value ? 'text-gray-300' : 'text-gray-500'}>
                              {key.replace('_', ' ').replace(/\b\w/g, l => l.toUpperCase())}
                            </span>
                          </div>
                        ))}
                      </div>
                    </div>

                    {result.score.suggestions.length > 0 && (
                      <div>
                        <h3 className="text-lg font-semibold text-white mb-3 flex items-center">
                          <TrendingUp className="mr-2 text-blue-400" /> Suggestions
                        </h3>
                        <ul className="space-y-2">
                          {result.score.suggestions.map((suggestion, index) => (
                            <motion.li
                              key={index}
                              initial={{ opacity: 0, x: -20 }}
                              animate={{ opacity: 1, x: 0 }}
                              transition={{ delay: 0.1 * index }}
                              className="text-gray-300 text-sm flex items-start"
                            >
                              <span className="text-purple-400 mr-2">•</span>
                              {suggestion}
                            </motion.li>
                          ))}
                        </ul>
                      </div>
                    )}
                  </motion.div>
                ) : (
                  <motion.div
                    key="placeholder"
                    initial={{ opacity: 0 }}
                    animate={{ opacity: 1 }}
                    exit={{ opacity: 0 }}
                    className="glass rounded-3xl p-8 shadow-2xl h-full flex items-center justify-center"
                  >
                    <div className="text-center">
                      <Sparkles className="w-24 h-24 text-purple-400 mx-auto mb-4 animate-pulse" />
                      <p className="text-gray-400 text-lg">Upload your resume to see AI-powered analysis</p>
                    </div>
                  </motion.div>
                )}
              </AnimatePresence>
            </motion.div>
          </div>
        </div>
      </div>
    </div>
  );
}

export default App;