/**
 * Copyright 2024 BetterWithData
 * 
 * Licensed under the Apache License, Version 2.0 (the "License");
 * you may not use this file except in compliance with the License.
 * You may obtain a copy of the License at
 * 
 *     http://www.apache.org/licenses/LICENSE-2.0
 * 
 * Unless required by applicable law or agreed to in writing, software
 * distributed under the License is distributed on an "AS IS" BASIS,
 * WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
 * See the License for the specific language governing permissions and
 * limitations under the License. 
 */

import * as ace from 'brace';

ace.define(
  'ace/mode/filter_highlight_rules',
  [
    'require',
    'exports',
    'module',
    'ace/lib/oop',
    'ace/mode/text_highlight_rules',
  ],
  (acequire, exports, module) => {
    'use strict';

    var oop = acequire('../lib/oop');
    var TextHighlightRules = acequire(
      './text_highlight_rules'
    ).TextHighlightRules;

    var FilterHighlightRules = function () {
      this.$rules = {
        start: [
          {
            token: 'keyword',
            regex: 'd\\.([a-zA-Z]*)',
          },
          {
            token: 'string',
            regex: '"[\\w\\d\\s]*"',
          },
          {
            token: 'string',
            regex: "'[\\w\\d\\s]*'",
          },
          {
            token: 'constant.numeric',
            regex: '[\\d]+',
          },
        ],
      };

      this.normalizeRules();
    };

    FilterHighlightRules.metaData = {
      fileTypes: ['filter'],
      name: 'Filter',
    };

    oop.inherits(FilterHighlightRules, TextHighlightRules);

    exports.FilterHighlightRules = FilterHighlightRules;
  }
);

ace.define(
  'ace/mode/filter',
  [
    'require',
    'exports',
    'module',
    'ace/lib/oop',
    'ace/mode/text',
    'ace/mode/filter_highlight_rules',
  ],
  (acequire, exports, module) => {
    'use strict';

    var oop = acequire('../lib/oop');
    var TextMode = acequire('./text').Mode;
    var FilterHighlightRules = acequire(
      './filter_highlight_rules'
    ).FilterHighlightRules;

    var Mode = function () {
      this.HighlightRules = FilterHighlightRules;
      this.$behaviour = this.$defaultBehaviour;
    };
    oop.inherits(Mode, TextMode);

    (function () {
      this.lineCommentStart = '#';
      this.$id = 'ace/mode/filter';
    }.call(Mode.prototype));

    exports.Mode = Mode;
  }
);
