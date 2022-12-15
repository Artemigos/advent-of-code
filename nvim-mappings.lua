local M = {}

local function ends_with(s, ending)
    return (string.sub(s, string.len(s)+1-string.len(ending)) == ending)
end

function M.run_current(data_file)
    local path = vim.api.nvim_buf_get_name(0)
    if not ends_with(path, 'solution.py') then
        return
    end

    local cwd = vim.fn.getcwd()
    local rel_path = string.sub(path, string.len(cwd)+2)
    local module_path = string.gsub(rel_path, '/', '.')
    module_path = string.sub(module_path, 1, string.len(module_path)-3)

    local challange_path = string.sub(rel_path, 1, string.len(rel_path)-string.len('solution.py'))
    local file_path = challange_path..data_file

    vim.api.nvim_input(':!pypy3 -m '..module_path..' '..file_path..'<CR>')
end

vim.keymap.set('n', '<leader>xx', function() M.run_current('data.txt') end)
vim.keymap.set('n', '<leader>xs', function() M.run_current('sample.txt') end)

return M
