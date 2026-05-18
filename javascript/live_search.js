(function ($) {
	'use strict';

	/**
	 * LiveSearch - debounced keyup search with JSON results rendered into a container.
	 *
	 * @param {string} inputSel   - jQuery selector for the text input
	 * @param {string} resultsSel - jQuery selector for the results container div
	 * @param {string} url        - endpoint that accepts ?highlight=<term> and returns
	 *                              JSON [{title, href, type}, ...]
	 */
	function LiveSearch(inputSel, resultsSel, url) {
		var $input   = $(inputSel);
		var $results = $(resultsSel);
		var lastVal  = '';
		var minLen   = 3;
		var delay    = 400;
		var timer    = 0;

		if (!$input.length || !$results.length) { return; }

		$input
			.on('focus', function () {
				if (this.value === this.defaultValue) { this.value = ''; }
			})
			.on('blur', function () {
				if (this.value === '') { this.value = this.defaultValue; }
			})
			.on('keyup', function () {
				var val = $.trim($input.val());
				if (val === lastVal) { return; }
				lastVal = val;
				clearTimeout(timer);
				if (val.length >= minLen) {
					$results.text('Searching…');
					timer = setTimeout(doSearch, delay);
				} else {
					$results.empty();
				}
			});

		$input.closest('form').on('submit', function (e) {
			e.preventDefault();
			doSearch();
		});

		function esc(s) {
			return $('<span>').text(s).html();
		}

		function doSearch() {
			var val = $.trim($input.val());
			if (!val || val === $input[0].defaultValue) { return; }
			$.getJSON(url, { highlight: val })
				.done(function (items) {
					if (!items || !items.length) {
						$results.html('<p>No results.</p>');
						return;
					}
					var html = '<ul>';
					$.each(items, function (i, r) {
						html += '<li><a href="' + esc(r.href) + '">' + esc(r.title) + '</a>';
						if (r.type) { html += ' <small>' + esc(r.type) + '</small>'; }
						html += '</li>';
					});
					html += '</ul>';
					$results.html(html);
				})
				.fail(function () {
					$results.html('<p>Search unavailable.</p>');
				});
		}
	}

	window.LiveSearch = LiveSearch;

}(jQuery));
