#!/usr/bin/ruby
# ruby 1.9 or 2.0 is required

guard 'bundler' do
  watch('Gemfile')
  # Uncomment next line if Gemfile contain `gemspec' command
  # watch(/^.+\.gemspec/)
end

guard :copy, from: 'archer/assets/js', to: 'archer/static/js/', mkpath: true do
  watch(%r{^.+\.js$})
end

guard :copy, from: 'archer/assets/css', to: 'archer/static/css/', mkpath: true do
  watch(%r{^.+\.css$})
end

guard :coffeescript, input: 'archer/assets/coffee', output: 'archer/static/js'

guard :sass, input: 'archer/assets/sass', output: 'archer/static/css'

# This will concatenate the javascript files specified in :files to public/js/all.js
guard :concat, type: 'js', files: %w(tree), input_dir: "archer/static/js/projects", output: "archer/static/js/projects"
guard :concat, type: 'js', files: %w(jquery-2.0.3 ajax), input_dir: "archer/static/js/core", output: "archer/static/js/core"

guard :concat, type: 'css', files: %w(custom_bootstrap), input_dir: 'archer/static/css/core', output: 'archer/static/css/core'
guard :concat, type: 'css', files: %w(tree actions), input_dir: 'archer/static/css/projects', output: 'archer/static/css/projects'

['archer/static/js/projects', 'archer/static/js/core'].each do |file|
  guard 'uglify', input: "#{file}.js", output: "#{file}.min.js" do
    watch ("#{file}.js")
  end
end

#['archer/static/css/projects'].each do |file|
#  guard 'minify', input: "#{file}.css", output: "#{file}.min.css"
#end

guard 'livereload' do
  watch(%r{archer/static/.+\.(css|html|js)$})
  watch(%r{archer/.+\.(py)$})
end

=begin
guard :shell do
  cmd = 'python ./manage.py test'
  watch(%r{^archer/(packages|projects)/(models|views|tests|admin)\.py$}) do |p|
    file = "archer.#{p[1]}.#{p[2]}"
    test_file = "archer.#{p[1]}"
    #n "#{file} changed", "Running #{test_file}", :pending
    run_cmd = "#{cmd} archer/#{p[1]}"
    result = system(run_cmd)
    puts result
    if result
      n file, "Success", :success
    else
      n file, "Failure #{test_file}", :failed
    end
  end
end
=end
