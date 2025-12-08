local M = {}

function M.run_current()
    local path = vim.api.nvim_buf_get_name(0)
    local cwd = vim.fn.getcwd()
    local rel_path = string.sub(path, string.len(cwd) + 2)
    local lang, year, day
    if string.sub(rel_path, 1, 3) == 'zig' then
        lang, year, day = string.match(rel_path, '^(%w+)/(%d+)/(%d+)%.zig$')
    else
        lang, year, day = string.match(rel_path, '^(%w+)/(%d+)/(%d+)/.+$')
    end
    -- can't use vim.cmd - it prints the output over the command (IMO incorrectly)
    -- can't use vim.system - it doesn't print the output
    vim.api.nvim_input(':!./run.sh run ' .. lang .. ' ' .. year .. ' ' .. day .. '<CR>')
end

function M.setup()
    local run_map = '<leader><CR>'
    if vim.fn.maparg(run_map, 'n') ~= '' then
        vim.keymap.del('n', run_map)
    end
    vim.keymap.set('n', run_map, M.run_current)
end

M.setup()

return M
