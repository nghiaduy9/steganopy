const fs = require('fs').promises
const path = require('path')

module.exports = async (req, res) => {
  const content = await fs.readFile(path.join(__dirname, '../../../static/sample.zip'))

  res.setHeader('content-type', 'application/octet-stream')
  return res.send(content)
}
